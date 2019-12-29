# coding=utf-8
import ConfigParser
import xmlrpclib
import random
import sys
import os

os.chdir(os.path.dirname(sys.argv[0]))
config = ConfigParser.ConfigParser()
config.read("config.ini")

db = config.get('SYSTEM', 'db')
login = config.get('SYSTEM', 'login')
password = config.get('SYSTEM', 'password')
url = config.get('SYSTEM', 'url')

sock_common = xmlrpclib.ServerProxy(url + '/xmlrpc/common')
uid = sock_common.login(db, login, password)
sock = xmlrpclib.ServerProxy(url + '/xmlrpc/object')


def get_orders_qty():
    return int(config.get('SALE_ORDER', 'orders_qty'))


def get_order_lines_qty():
    return int(config.get('SALE_ORDER', 'order_lines_qty'))


def get_product_uom_qty():
    return int(config.get('SALE_ORDER', 'product_uom_qty'))


def get_client_id():

    if config.get('SALE_ORDER_OTHER', 'clients_ids'):
        clients_ids = map(int, (config.get('SALE_ORDER_OTHER', 'clients_ids')).split(","))
    else:
        clients_ids = sock.execute_kw(db, uid, password, 'res.partner', 'search',
                                      [[['customer', '=', True], ['type', '=', 'contact']]])

    return random.choice(clients_ids)


def get_prieclist_id():

    if config.get('SALE_ORDER_OTHER', 'pricelists_ids'):
        pricelists_ids = map(int, (config.get('SALE_ORDER_OTHER', 'pricelists_ids')).split(","))
    else:
        pricelists_ids = sock.execute_kw(db, uid, password, 'product.pricelist', 'search', [[]])

    return random.choice(pricelists_ids)


def get_sale_shop_id():

    if config.get('SALE_ORDER_OTHER', 'sale_shops_ids'):
        sale_shops_ids = map(int, (config.get('SALE_ORDER_OTHER', ' sale_shops_ids')).split(","))
    else:
        sale_shops_ids = sock.execute_kw(db, uid, password, 'sale.shop', 'search', [[]])

    return random.choice(sale_shops_ids)


def get_ship_product_id():

    if config.get('SALE_ORDER', 'ship_product_id'):
        ship_product_id = int(config.get('SALE_ORDER', 'ship_product_id'))
    else:
        ship_product_id = (sock.execute_kw(db, uid, password, 'product.product', 'search',
                                          [[['name', '=', 'Wysyłka']]], {'limit': 1}))[0]
    return ship_product_id


def get_product_id():

    if config.get('SALE_ORDER_OTHER', 'products_ids'):
        products_ids = map(int, (config.get('SALE_ORDER_OTHER', 'products_ids')).split(","))
    else:
        products_ids = sock.execute_kw(db, uid, password, 'product.product', 'search', [[['type', '=', 'product']]])

    return random.choice(products_ids)


def get_delivery_and_payment_type():

    delivery_and_payment_type = config.get('SALE_ORDER', 'delivery_and_payment_type')
    if delivery_and_payment_type == 'cod':
        return 'COD'
    elif delivery_and_payment_type == 'prepayment':
        return 'prepayment'
    else:
        return random.choice(['prepayment', 'COD'])


def get_payment_term_id(payment_type):

    if config.get('SALE_ORDER_OTHER', 'payment_terms_ids'):
        payment_terms_list = map(int, (config.get('SALE_ORDER_OTHER', 'payment_terms_ids')).split(","))
        payment_terms_dict = sock.execute_kw(db, uid, password, 'account.payment.term', 'search_read',
                                         [[['id', 'in', payment_terms_list]]], {'fields': ['payment_type']})
    else:
        payment_terms_dict = sock.execute_kw(db, uid, password, 'account.payment.term', 'search_read',
                                            [[]], {'fields': ['payment_type']})

    payment_terms_ids = []
    for payment in payment_terms_dict:
        if payment['payment_type'] == payment_type:
            payment_terms_ids.append(payment['id'])

    return random.choice(payment_terms_ids)


def get_delivery_carrier_id(delivery_type):

    if config.get('SALE_ORDER_OTHER', 'delivery_carriers_ids'):
        delivery_carriers_list = map(int, (config.get('SALE_ORDER_OTHER', 'delivery_carriers_ids')).split(","))
        delivery_carriers_dict = sock.execute_kw(db, uid, password, 'delivery.carrier', 'search_read',
                                         [[['id', 'in', delivery_carriers_list]]], {'fields': ['delivery_payment_type']})
    else:
        delivery_carriers_dict = sock.execute_kw(db, uid, password, 'delivery.carrier', 'search_read',
                                            [[]], {'fields': ['delivery_payment_type']})

    delivery_carriers_ids = []
    for delivery in delivery_carriers_dict:
        if delivery['delivery_payment_type'] == delivery_type:
            delivery_carriers_ids.append(delivery['id'])

    return random.choice(delivery_carriers_ids)
