from emailer import send_hourly_monitoring_email, send_best_buy_change_email, send_email
from event import *
from util.birthday import birthday
from util.str_contains import str_contains_ignore_case, str_contains
from priority import Priority

import requests
from random import randint
from time import sleep
from datetime import datetime
from collections import deque


def get_data():
    headers = {"User-Agent": "Mozilla/5.0"}

    print('Downloading URL...')
    data = requests.get(URL, headers=headers)
    print('Downloading complete.')

    return data.text


# Process the html data to gather the juicy details. Also, why use regex when we can do it caveman-style.
# TODO: maybe change to using regex later.
def process(data):
    print(len(data))
    status = {}
    links = {}
    a, b, c = ['<div class="right-column">', '<h4 class="sku-header">', '<div class="sku-list-item-button"']
    i = 0
    unknown = 'UNKNOWN'
    while i < len(data):
        if data[i:i + len(a)] == a:
            z = data.find(b, i)
            hi = i + 1
            yolo = ''
            if z >= i:
                hi = z + 1
                y = data.find('<a href=', z)
                if y >= z:
                    hi = y + 1
                    x = data.find('>', y)
                    w = data.find('</a>', x)
                    link = 'https://bestbuy.com' + data[y + 9:x - 1]
                    yolo = data[x + 1:w]
                    status[yolo] = unknown
                    links[yolo] = link
            zz = data.find(c, hi)
            if zz >= 0:
                hi = zz + 1
                yy = data.find('<button class=', zz)
                if yy >= zz:
                    hi = yy + 1
                    xx = data.find('>', yy)
                    ww = data.find('</button>', xx)
                    yeet = data[xx + 1:ww]
                    if str_contains(yeet, '</svg>'):
                        yeet = yeet[yeet.find('</svg>') + 6:]
                    status[yolo] = yeet
            i = hi
        else:
            i += 1
    return status, links


def find_events(now, before, now_time):
    if not TEST:
        if not before:
            return []
    added = []
    for k in now:
        if k not in before and str_contains_ignore_case(now[k], 'add to cart'):
            added.append(Event(k, now[k], Priority.LOW, 'PRODUCT ADDED', now_time))
    modified = []
    for k in before:
        if k in now:
            if now[k] != before[k] and str_contains_ignore_case(now[k], 'add to cart'):
                priority = Priority.MEDIUM
                if str_contains_ignore_case(k, 'sleeved'):
                    priority = Priority.HIGH
                if str_contains_ignore_case(k, 'shining fates'):
                    priority = Priority.VERY_HIGH
                    if str_contains_ignore_case(k, 'elite trainer box'):
                        priority = Priority.HIGHEST
                elif str_contains_ignore_case(k, 'elite trainer box'):
                    priority = Priority.VERY_HIGH
                modified.append(
                    Event(k, now[k], priority, 'STATUS CHANGE: {0} -> {1}'.format(before[k], now[k]), now_time))

    return sorted(modified + added, key=lambda x: (x.priority, x.product))


def set_event_links(events, links):
    if not links:
        return
    for e in events:
        if e.product in links:
            e.link = links[e.product]


def make_fake_events(now_time):
    events = [
        Event('Pokémon - Pokemon TCG: Shining Fates Elite Trainer Box ', 'add to cart', Priority.HIGHEST,
              'STATUS_CHANGED: sold out -> add to cart', now_time),
        Event('Pokémon TCG: Sword &amp; Shield—Vivid Voltage Sleeved Booster', 'add to cart', Priority.MEDIUM,
              'STATUS_CHANGED: sold out -> add to cart', now_time),
        Event('Pokémon - Pokemon TCG: Shining Fates Pikachu V', 'add to cart', Priority.VERY_HIGH,
              'STATUS_CHANGED: sold out -> add to cart', now_time),
    ]
    return events


def filter_events(events):
    filtered_events = [e for e in events if not should_ignore(e)]
    if len(events) != len(filtered_events):
        filtered_products = set([e.product for e in filtered_events])
        print('SOME PRODUCTS WERE IGNORED: {}'.format(
            ', '.join([e.product for e in events if e.product not in filtered_products])))
    return filtered_events


def print_statuses(statuses):
    lines = '\n'.join(['{:100}:\t{:30}'.format(('[IGNORE] ' + x if should_ignore_product(x) else x), y) for x, y in
                       statuses.items()])
    print(lines)


def loop():
    print('Main loop start. Birthday: {}'.format(str(birthday)))
    old_status = {}
    num_runs = 0
    prev_time = None
    event_history = deque()
    while True:
        now_time = datetime.now()
        print('Top of loop. Time is {}.{}'.format(str(now_time),
                                                  ('' if prev_time is None else ' Prev time was ' + str(prev_time))))
        statuses, links = process(get_data())

        print_statuses(statuses)

        if TEST:
            print('LINKS:')
            print('\n'.join(['{}: {}'.format(k, v) for k, v in links.items()]))

        # Find and filter events.
        events = filter_events(find_events(statuses, old_status, now_time))
        if TEST:
            events = make_fake_events(now_time)

        # After events have been created and filtered.
        set_event_links(events, links)

        # Append to event history to send in monitoring email.
        for event in events:
            event_history.append(event)
            if len(event_history) > HISTORY_MAX_SIZE:
                event_history.popleft()
        old_status = statuses

        if events or TEST:
            send_best_buy_change_email(events)

        num_runs += 1
        if TEST and num_runs >= TEST_RUN_LIMIT:
            break

        if prev_time is not None and now_time.hour != prev_time.hour:
            send_hourly_monitoring_email(event_history, num_runs)
        prev_time = now_time

        sleep(randint(FREQUENCY_LOW, FREQUENCY_HIGH))


def safe_loop():
    while True:
        err = None
        try:
            loop()
        except Exception as e:
            err = e
            print('LOOP CRASHED!!!', str(err))
            send_email(ADMINS, 'Houston, We Have a Problem', """
            <html>
            <h2>BestBuyer crashed at {}</h2>
            <h2>ERROR: {}</h2>
            <h2>Waiting {} minutes before trying again...</h2>
            </html>
            """.format(str(datetime.now()), str(err), str(WAIT_TIME / 60)))
        if not err:
            print('Exited loop. No error occurred.')
        print('Waiting {} minutes before trying again. The time is now: {}'.format(str(WAIT_TIME / 60),
                                                                                   str(datetime.now())))
        sleep(WAIT_TIME)


if __name__ == '__main__':
    safe_loop()
