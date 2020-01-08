# coding=utf-8
from CreateSaleOrders import GetDataFromConfig

data = GetDataFromConfig


def create_orders():
    for order in range(1, data.get_orders_qty()+1):
        type = data.get_delivery_and_payment_type()
        order_id = data.sock.execute_kw(data.db, data.uid, data.password, 'sale.order', 'create', [{
            'partner_id': data.get_client_id(),
            'carrier_id': data.get_delivery_carrier_id(type),
            'payment_term_id': data.get_payment_term_id(type),
            'pricelist_id': data.get_prieclist_id(),
            'shop_id': data.get_sale_shop_id()
        }])

        """Dodanie produktu wysylka do listy"""
        order_lines = [(0, '_', {'product_id': data.get_ship_product_id(), 'product_uom_qty': 1})]

        """Dodanie pozostalych pozycji zamowienia do listy"""
        for line in range(0, data.get_order_lines_qty()):
            order_lines.append((0, '_', {'product_id': data.get_product_id(), 'product_uom_qty': data.get_product_uom_qty()}))

        """Utworzenie pozycji zamowienia na podstawie przekazanej listy"""
        data.sock.execute_kw(data.db, data.uid, data.password, 'sale.order', 'write', [[order_id], {'order_line': order_lines}])

        print("Stworzono zamowienie " + str(order) + "/" + str(data.get_orders_qty()) + " o id: " + str(order_id))

        if data.get_confirm_flag():
            try:
                data.sock.execute(data.db, data.uid, data.password, 'sale.order', 'action_confirm', order_id)
                print("Potwierdzono zamowienie o id: " + str(order_id))
            except:
                print("Błąd podczas potwierdzania zamowienia " + str(order_id))


create_orders()