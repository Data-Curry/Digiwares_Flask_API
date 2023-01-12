from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


"""
warehouses = {
    1: {
            "warehouse_name": "Rainyday",
            "wh_num": "1",
            "city": "Seattle",
            "state": "WA"
    }
}

items = {
    1: {
            "name": "Patio Table",
            "item_num": "1",
            "retail_price": "99.99",
            "wholesale_price": "50.00",
            "category": "furniture",
            "vendor": "Acme",
            "warehouse": "Rainyday",
            "qty": "10"
        },
    2: {
            "name": "Patio Chair",
            "item_num": "2",
            "retail_price": "29.99",
            "wholesale_price": "10.00",
            "category": "furniture",
            "vendor": "Acme",
            "warehouse": "Empty Towers",
            "qty": "40"
        }
}
"""
