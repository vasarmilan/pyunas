# -*- coding: utf-8 -*-

from __future__ import print_function
import zeep
import os
from xmltodict import unparse as dicttoxml
import xmltodict


class _UnasService(object):
    """ Internal implementation of the unasapi zeep service, which provides direct access to methods, does the authentication, and accepts params as dict or as xml.
    Example (for getting "Számlázható" orders):
    import pyunas

    service = pyunas.main._UnasService()
    params = {'InvoiceStatus': 1}
    response = service.getOrder(params)
    (returns raw xml response)
    """
    wsdl = "https://api.unas.eu/shop/?wsdl"
    method_list = ["getAuth", "getCustomer", "getNewsletter", "getOrder", "getProduct", "getProductDB", "getStock", "setNewsletter", "setNewsletterXML", "setOrder", "setOrderXML", "setProduct", "setProductDB", "setProductXML", "setStock", "setStockXML"]

    def __init__(self):
        self._client = zeep.Client(self.wsdl)
        self._service = self._client.service
        for method in self.method_list:
            setattr(self, method, self._construct_api_func(method))

    def _construct_api_func(self, method):
        def func(params, auth=None):
            auth = auth or self._auth()
            res = getattr(
                    self._service, method)(self._auth(), self._dictorxml(params))
            return xmltodict.parse(res)
        return func

    def _dictorxml(cls, inp, custom_root='params'):
        try:  # for python3 compatibility
            if type(inp) == str or type(inp) == unicode:
                return inp
        except NameError:
            if type(inp) == str:
                return inp

        # else
        try:
            res =\
                dicttoxml({custom_root: inp})
            return res
        except TypeError:
            res = \
                dicttoxml(inp, custom_root=custom_root).decode("utf-8")

    @classmethod
    def _auth(cls):
        """return auth xml as string"""
        dirname = os.path.dirname(__file__)
        filename = dirname + "/data/auth.xml"
        with open(filename, 'r') as file:
            authxml = file.read()
        return authxml


class _UnasMeta(type):
    def __getattr__(cls, key):
        _service = _UnasService()
        return getattr(_service, key)


class api:
    __metaclass__ = _UnasMeta
