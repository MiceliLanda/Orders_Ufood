from tokenize import Double
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select
from models.buy import tableOrder, tableOrderDetails,tableSaucer,tableShop
from schemas.buy import OrderSchema,OrderDetailSchema
from config.db import conn

buyRoute = APIRouter()

@buyRoute.get("/")
def get_root():
    JSONResponse({"Ok": ":)"}, status_code=200)

@buyRoute.post("/user/buy")
def buy_product(order: OrderSchema):
    try:
        conn.execute(tableOrder.insert().values(total=order.total, date_purchase=order.date_purchase, user_id=order.user_id))
        order_id = conn.execute(tableOrder.select().order_by(tableOrder.c.id.desc()).limit(1)).first()[0]
        for product in order.products:
            conn.execute(tableOrderDetails.insert().values(order_id=order_id, saucer_id=product))
        return JSONResponse({"message": "Orden creada correctamente"}, status_code=200)
    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)

@buyRoute.get("/user/orders")
def get_orders(user_id: int):
    try:
        orders = conn.execute(select([tableOrder.c.id,tableOrderDetails.c.saucer_id,tableOrder.c.user_id,tableSaucer.c.name,tableSaucer.c.price,tableOrder.c.date_purchase,tableOrder.c.total]).select_from(tableOrder.join(tableOrderDetails,tableOrder.c.id == tableOrderDetails.c.order_id).join(tableSaucer,tableSaucer.c.id == tableOrderDetails.c.saucer_id)).where(tableOrder.c.user_id == user_id)).fetchall()
        list_orders = []
        for order in orders:
            list_orders.append({
                "order_id": order[0],
                "saucer_id": order[1],
                "user_id": order[2],
                "saucer": order[3],
                "price": str(order[4]),
                "date_purchase": str(order[5]),
                "total": str(order[6])
            })
        return JSONResponse({"orders":list_orders}, status_code=200)
    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)
