from emailer import send_hourly_monitoring_email, send_best_buy_change_email, send_email, importance_prefix
from event import Event, should_ignore
from datetime import datetime, timedelta
from constants import ADMINS
from priority import Priority
from main import find_events
import constants

constants.TEST.append('TRUE')


class EmailTest:
    fake_events = [
        Event('Pokémon - Pokemon TCG: Shining Fates Elite Trainer Box', 'add to cart', Priority.HIGH,
              'Status Changed: Bad -> Good', datetime.now()),
        Event('Pokémon TCG: Sword &amp; Shield—Vivid Voltage Sleeved Booster', 'sold out', Priority.LOW,
              'Status Changed: Good -> Bad', datetime.now() - timedelta(weeks=1)),
    ]


def test_hourly_email():
    send_hourly_monitoring_email(EmailTest().fake_events, 50)


def test_ignore_list():
    products = """
    Pokémon - Pokemon TCG: Shining Fates Elite Trainer Box                                              :	Sold Out                      
    Pokémon TCG: Sword &amp; Shield—Vivid Voltage Sleeved Booster                                       :	Add to Cart                   
    Pokémon - Pokemon TCG: Shining Fates Pikachu V                                                      :	Sold Out                      
    Pokémon - Pokemon TCG: Battle Styles Sleeved Boosters                                               :	Sold Out                      
    Pokémon - Pokemon TCG: Alola First Partner Pack                                                     :	Sold Out                      
    Pokémon - Pokemon TCG: Champion&#x27;s Path Collection-- Dubwool V                                  :	Sold Out                      
    Pokémon - Pokemon TCG: First Partner Collector’s Binder                                             :	Add to Cart                   
    Pokémon - Pokemon TCG: Shining Fates Mini Tin                                                       :	Sold Out                      
    Pokémon - Pokemon TCG: V Battle Decks Blastoise or Venusaur                                         :	Check Stores                  
    Pokémon - Pokemon TCG: Collector Chest Spring 2021                                                  :	Sold Out                      
    Pokémon - TCG: Battle Academy Box Set                                                               :	Add to Cart                   
    Pokémon - Pokemon TCG: Shining Fates V Tin                                                          :	Sold Out                      
    Pokémon - Pokemon TCG: Shining Fates Premium Collection                                             :	Sold Out                      
    Pokémon - Pokemon TCG: Poke Ball Tin                                                                :	Sold Out                      
    Pokémon - Pokemon TCG: Battle Styles Elite Trainer Box                                              :	Sold Out                      
    Pokémon - Pokemon TCG: Urshifu Strike V Box                                                         :	Sold Out                      
    Pokémon - TCG: Darkness Ablaze Sleeved Boosters                                                     :	Sold Out                      
    Pokémon TCG: Fall 2020 Collector Chest                                                              :	Sold Out                      
    Pokémon - Pokemon TCG: VMAX Battle Box Blastoise or Venusaur                                        :	Sold Out                      
    Pokémon - XY Evolutions Sleeved Booster Trading Cards - Styles May Vary                             :	Sold Out                      
    """
    lines = products.split('\n')
    assert len(lines), 20
    good_lines = []
    for line in lines:
        if not should_ignore(Event(line, None, None, None, None)):
            good_lines.append(line)
    actual = '\n'.join(good_lines)
    expected = """
    Pokémon - Pokemon TCG: Shining Fates Elite Trainer Box                                              :	Sold Out                      
    Pokémon TCG: Sword &amp; Shield—Vivid Voltage Sleeved Booster                                       :	Add to Cart                   
    Pokémon - Pokemon TCG: Shining Fates Pikachu V                                                      :	Sold Out                      
    Pokémon - Pokemon TCG: Battle Styles Sleeved Boosters                                               :	Sold Out                      
    Pokémon - Pokemon TCG: Champion&#x27;s Path Collection-- Dubwool V                                  :	Sold Out                      
    Pokémon - Pokemon TCG: Shining Fates Mini Tin                                                       :	Sold Out                      
    Pokémon - Pokemon TCG: Shining Fates V Tin                                                          :	Sold Out                      
    Pokémon - Pokemon TCG: Shining Fates Premium Collection                                             :	Sold Out                      
    Pokémon - Pokemon TCG: Battle Styles Elite Trainer Box                                              :	Sold Out                      
    Pokémon - Pokemon TCG: Urshifu Strike V Box                                                         :	Sold Out                      
    Pokémon - TCG: Darkness Ablaze Sleeved Boosters                                                     :	Sold Out                      
    Pokémon - XY Evolutions Sleeved Booster Trading Cards - Styles May Vary                             :	Sold Out                      
    """
    assert actual == expected, '\nEXPECTED:{}\nACTUAL:{}\n'.format(expected, actual)


def test_send_html_email():
    send_email(ADMINS, 'HTML TEST', """
    <html><h1>This is a test email!</h1><span>I am in a span!</span></html>
    """)


def test_send_events_table():
    send_best_buy_change_email(EmailTest().fake_events)


def test_importance_prefix():
    prefix = importance_prefix(EmailTest().fake_events)
    assert prefix == '[TEST] [*ELITE TRAINER BOX*] [BOOSTER] ', prefix


def test_find_events():
    before = {
        'Pokémon - Pokemon TCG: Battle Styles Sleeved Boosters': 'sold out',
        'Pokémon - Pokemon TCG: Shining Fates Premium Collection': 'add to cart',
    }
    now = {
        'Pokémon - Pokemon TCG: Battle Styles Sleeved Boosters': 'add to cart',
        'Pokémon - Pokemon TCG: Battle Styles Elite Trainer Box': 'add to cart',
        'Pokémon - TCG: Darkness Ablaze Sleeved Boosters': 'sold out',
    }
    now_time = datetime.now()
    events = find_events(now, before, now_time)
    expected = {
        Event('Pokémon - Pokemon TCG: Battle Styles Sleeved Boosters', 'add to cart', Priority.HIGH,
              'STATUS CHANGE: sold out -> add to cart', now_time),
        Event('Pokémon - Pokemon TCG: Battle Styles Elite Trainer Box', 'add to cart', Priority.LOW,
              'PRODUCT ADDED', now_time),
    }
    assert set(events) == expected, '\nActual:\n' + '\n'.join([str(e) for e in events]) + \
                                    '\nExpected:\n' + '\n'.join([str(e) for e in expected])


test_hourly_email()
test_ignore_list()
test_send_html_email()
test_send_events_table()
test_importance_prefix()
test_find_events()
print('all tests passed!')
