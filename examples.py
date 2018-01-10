# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import xmltodict
from . import helpers
from . import main


def unprocessed_orders_odoo_sync():
    orders = unprocessed_orders()
    keys = [ord['Key'] for ord in orders]
    return _set_to_processing_list(keys)
    return orders


def unprocessed_orders():
    status = 1
    return xmltodict.parse(get_orders(Status=status))['Orders']['Order']


def _set_to_processing_list(nums, service=None):
    """
    sets each order number to status 301479 (`Feldolgozás alatt`)
    using the setOrderXML api call

    Keyword arguments:
    service -- main._UnasService object
    nums -- order numbers to change
    """
    status = 301479
    if not service:
        service = main._UnasService()
    order_dicts = []
    for num in nums:
        order_dicts.append(
                {'Key': num,
                    'Status': status})

    # TODO: raise sth error if operation wasn't completed, indicating the
    # wrong order number
    # or just do this separately
    res = service.setOrderXML({'Order': order_dicts})
    return xmltodict.parse(res)

def orders():
    fname = helpers.datafolder + "/orders0.json"
    if os.path.isfile(fname):
        print("using cache")
        return json.loads(open(fname).read())
    else:
        print("getting orders from api")
        return get_orders()


def get_uninvoiced_orders(InvoiceStatus = 2, DateStart = '2017.01.01', **kwargs):
    """
    WARNING: ONLY 500 ORDERS
    """
    service = main._UnasService()
    params = {'InvoiceStatus': InvoiceStatus,
              'DateStart': DateStart
              }
    for arg in kwargs:
        params[arg] = kwargs[arg]
    return helpers.response_to_orders(service.getOrder(params))


def get_orders(**kwargs):
    params = {}
    service = main._UnasService()
    for arg in kwargs:
        params[arg] = kwargs[arg]
    # return helpers.response_to_orders(service.getOrder(params))
    return service.getOrder(params)


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
