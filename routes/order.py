from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select
from models.buy import tableOrder, tableOrderDetails,tableSaucer
from schemas.buy import OrderSchema,OrderDetailSchema
from config.db import conn

buyRoute = APIRouter()

@buyRoute.get("/")
async def get_root():
    return {"message": ":)"}

@buyRoute.post("/user/buy")
async def buy_product(order: OrderSchema):
    try:
        conn.execute(tableOrder.insert().values(total=float(order.total), date_purchase=order.date_purchase, user_id=order.user_id))
        order_id = conn.execute(tableOrder.select().order_by(tableOrder.c.id.desc()).limit(1)).first()[0]
        for product in order.products.split(","):
            conn.execute(tableOrderDetails.insert().values(order_id=order_id, saucer_id=int(product)))
        return JSONResponse({"message": "Orden creada correctamente"}, status_code=200)
    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)



@buyRoute.get("/user/orders")
async def get_orders(user_id: int):
    try:
        orders = conn.execute(select([tableOrder.c.id, tableOrder.c.total, tableOrder.c.date_purchase]).where(tableOrder.c.user_id == user_id)).fetchall()
        order_list = []
        for order in orders:
            order_list.append({"orden": order[0], "total": str(order[1]), "date_purchase": str(order[2])})
        return JSONResponse({"orders": order_list}, status_code=200)
    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)

@buyRoute.get("/user/orders-details")
async def get_orders_detail(order_id: int):
    try:
        orders = conn.execute(select([tableOrder.c.id,tableSaucer.c.name,tableSaucer.c.price]).select_from(tableOrder.join(tableOrderDetails,tableOrder.c.id == tableOrderDetails.c.order_id).join(tableSaucer,tableSaucer.c.id == tableOrderDetails.c.saucer_id)).where(tableOrder.c.id == order_id)).fetchall()
        list_orders = [] 

        for order in orders:
            list_orders.append({
                "platillo": order[1],
                "precio": str(order[2]),
            })

        return JSONResponse({"order_details":list_orders})
    except Exception as e:
        return JSONResponse({"Error": str(e)}, status_code=500)
