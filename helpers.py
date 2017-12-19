# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime

datafolder = "/home/vasar/Dropbox/business/.unasdata"

dateformat = "%Y.%m.%d %H:%M:%S"

def response_to_orders(response):
    first = response[next(iter(response.keys()))]
    return first[list(first.keys())[0]]


def orders_for_stock_analysis(orderlist):
    def format_items(items):
        if type(items) == dict:
            items = [items]
        return [
            {'sku': item['Sku'],
             'quantity': item['Quantity']}
            for item in items
            if (item['Sku'] != 'shipping-cost')
        ]
    return [
        {
            'date': datetime.strptime(order['Date'], dateformat).date(),
            'cust_email': order['Customer']['Email'],
            'items': format_items(order['Items']['Item'])
        }
        for order in orderlist]


