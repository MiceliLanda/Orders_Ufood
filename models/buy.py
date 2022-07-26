from sqlalchemy import Table
from config.db import meta, engine

tableOrder = Table('order', meta, autoload=True, autoload_with=engine)
tableOrderDetails = Table('order_details', meta, autoload=True, autoload_with=engine)
tableSaucer = Table('saucer', meta, autoload=True, autoload_with=engine)
tableShop = Table('shop', meta, autoload=True, autoload_with=engine)
