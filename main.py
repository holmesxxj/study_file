from fastapi import FastAPI
from typing import Union
from router_api import shop_test,param_test,param_json
from SQLAlchemy_study import router
app = FastAPI()

#load all of router 
app.include_router(shop_test.shop2)

app.include_router(param_test.post_param)
app.include_router(param_json.json_param)
app.include_router(router.sqlalchemy_router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


