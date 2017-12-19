# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
from . import helpers
from . import main


def orders():
    fname = helpers.datafolder + "/orders0.json"
    if os.path.isfile(fname):
        print("using cache")
        return json.loads(open(fname).read())
    else:
        print("getting orders from api")
        return get_orders()


def get_orders(InvoiceStatus = 2, DateStart = '2017.01.01'):
    """
    WARNING: ONLY 500 ORDERS
    """
    service = main._UnasService()
    params = {'InvoiceStatus': InvoiceStatus,
              'DateStart': DateStart
              }
    return helpers.response_to_orders(service.getOrder(params))


def orders_for_stock_analysis():
    return helpers.orders_for_stock_analysis(orders())


def items_for_stock_analysis():
    #!!!
    orders = orders_for_stock_analysis()
    res = []
    for order in orders:
        items = order['']

def product():
    service = main._UnasService()
    params = {'DateStart': "2012.08.01"}
    return service.getProduct(params)
