from fastapi import FastAPI
from routes.order import buyRoute
import uvicorn

app = FastAPI()
app.include_router(buyRoute)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)