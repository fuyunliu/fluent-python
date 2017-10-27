# -*- coding: utf-8 -*-

from collections import namedtuple
import inspect

import promotions

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


def fidelity_promo(order):
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    """10% discount for each LineItem with 20 or more units"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1
    return discount


def large_order_promo(order):
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.07
    return 0


# best promotion version 1
promos_v1 = [fidelity_promo, bulk_item_promo, large_order_promo]


def best_promo_v1(order):
    """Select best discount available"""
    return max(promo(order) for promo in promos_v1)


# best promotion version 2
promos_v2 = [globals()[name] for name in globals() if name.endswith('_promo')]


def best_promo_v2(order):
    """Select best discount available"""
    return max(promo(order) for promo in promos_v2)


# best promotion version 3
promos_v3 = [func for name, func in
             inspect.getmembers(promotions, inspect.isfunction)]


def best_promo_v3(order):
    """Select best discount available"""
    return max(promo(order) for promo in promos_v3)
