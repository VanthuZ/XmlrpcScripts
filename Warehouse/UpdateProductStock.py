from CreateSaleOrders import GetDataFromConfig

data = GetDataFromConfig


def update_products_stock(products):

    location_id = (data.sock.execute_kw(data.db, data.uid, data.password, 'stock.location', 'search',
                                       [[['name', '=', 'Strefa składowania']]], {'context': {'lang': 'pl_PL'}}))[0]

    for product_id in products:
        change_id = data.sock.execute_kw(data.db, data.uid, data.password, 'stock.change.product.qty', 'create', [{
                    'product_id': product_id,
                    'location_id': location_id,
                    'new_quantity': 100,
                    }])

        data.sock.execute_kw(data.db, data.uid, data.password, 'stock.change.product.qty', 'change_product_qty', [change_id])