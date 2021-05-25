from constants import *
from util.str_contains import str_contains_ignore_case


class Event:
    def __init__(self, product, status, priority, reason, now_time):
        self.product = product
        self.status = status
        self.priority = priority
        self.reason = reason
        self.time = now_time
        self.link = ''

    def __str__(self):
        return 'product={}, status={}, priority={}, reason={}, time={}, link={}'.format(self.product, self.status,
                                                                                        self.priority, self.reason,
                                                                                        self.time, self.link)

    def __eq__(self, other):
        return self.product == other.product and self.status == other.status and self.priority == other.priority and \
               self.reason == other.reason and self.time == other.time and self.link == other.link


def stringify_events(events):
    return '\n\n'.join([str(e) for e in events])


def should_ignore_product(product):
    for ignore in IGNORE_LIST_SUBSTRINGS:
        if str_contains_ignore_case(product, ignore):
            return True
    return False


def should_ignore(event):
    return should_ignore_product(event.product.lower())


def get_short_product_name(product):
    things_to_remove = ['Pokémon - ', 'Pokemon TCG: ', 'Pokémon TCG: ']
    for remove in things_to_remove:
        product = product.replace(remove, '')
    return product
