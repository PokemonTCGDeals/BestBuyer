import smtplib
from email.mime.text import MIMEText
from constants import *
from event import get_short_product_name
from util.birthday import birthday
from util.str_contains import str_contains_ignore_case, str_contains


def importance_prefix(events):
    class ImportanceItem:
        def __init__(self, list_of_product_substrings, prefix_to_prepend):
            self.list_of_product_substrings = list_of_product_substrings
            self.prefix_to_prepend = prefix_to_prepend
            self.found = False

    # In order from least important to most important product.
    importance_precedence = [
        ImportanceItem([' booster'], 'BOOSTER'),
        ImportanceItem([' tin'], 'TIN'),
        ImportanceItem(['pikachu v', 'dubwool v', 'shining fates premium collection',
                        'urshifu strike v'], 'BOX'),
        ImportanceItem(['elite trainer box'], '*ELITE TRAINER BOX*'),
    ]

    # Try to find a product that fills that importance item.
    for e in events:
        for importance in importance_precedence:
            for substring in importance.list_of_product_substrings:
                if str_contains_ignore_case(e.product, substring):
                    importance.found = True
                    break

    def prepend_to_prefix(pre, should_do, to_prepend):
        if should_do:
            pre = '[{}] {}'.format(to_prepend, pre)
        return pre

    # Determine prefix.
    prefix = ''
    for importance in importance_precedence:
        prefix = prepend_to_prefix(prefix, importance.found, importance.prefix_to_prepend)

    if TEST:
        prefix = '[TEST] ' + prefix

    return prefix


def generate_email_subject(events):
    return 'POKEMON TCG - Found Changes to BestBuy'


def get_html_styles():
    return """
    <head>
    <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }
    th, td {
      padding: 5px;
      text-align: center;    
    }
    </style>
    </head>
    """


def create_html_table_from_events(events):
    if not events:
        return ''
    table = ['<table>']
    cols = ['Product', 'Current Status', 'Event Description']
    table.append('<tr>')
    for col in cols:
        table.append('<th>{}</th>'.format(col))
    table.append('</tr>')
    for event in events:
        short_name = get_short_product_name(event.product)
        table.append('<tr>'
                     '<td>{}</td>'
                     '<td>{}</td>'
                     '<td>{}</td>'
                     '</tr>'.format(
            ('<a href="{}">{}</a>'.format(event.link, short_name) if event.link else short_name),
            event.status,
            event.reason))
    table.append('</table>')
    return ''.join(table)


def send_best_buy_change_email(events):
    print('Sending BestBuy changes email...')
    send_email(CHANGE_LISTENERS, generate_email_subject(events),
               """
               <html>
               {}
               <h2>{}FOUND CHANGES!!!</h2>
               <h3>URL: {}</h3>
               <h3>BestBuyer frequency range: {} to {} seconds</h3>
               {}
               """.format(
                   get_html_styles(), importance_prefix(events), URL,
                   FREQUENCY_LOW, FREQUENCY_HIGH,
                   create_html_table_from_events(events)))


def send_hourly_monitoring_email(event_history, num_runs):
    if not ACTIVATE_HOURLY_MONITORING:
        return
    print('Sending hourly monitoring email...')
    send_email(ADMINS, 'POKEMON TCG - MONITORING EMAIL',
               'This is monitoring data for the BestBuyer server.\n'
               'This server was born at {} and has run {} times.\n\n'
               'EVENT HISTORY:\n{}'.format(str(birthday), num_runs,
                                           '\n'.join(
                                               ['{}: {}'.format(str(e.time), str(e)) for e in event_history])))


def send_email(recipients, subject, message):
    if TEST:
        recipients = ADMINS

    if not recipients or not SENDER:
        return

    gmail = None
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(SENDER, SUPER_SECRET_PASSWORD)
    except Exception as e:
        print("Email setup error:", str(e))

    email_message = MIMEText(message, ('html' if str_contains(message, '<html>') else 'plain'))
    email_message['Subject'] = subject
    email_message['From'] = SENDER
    email_message['To'] = SENDER

    if TEST:
        print('_____________EMAIL CONTENTS_____________')
        print('Subject:', subject)
        print('Recipients:', ', '.join(recipients))
        print(message)
        print('_____________EMAIL CONTENTS END_____________')

    try:
        if gmail is not None:
            gmail.send_message(email_message, from_addr=SENDER, to_addrs=recipients)
    except Exception as e:
        print('Email send error:', str(e))
