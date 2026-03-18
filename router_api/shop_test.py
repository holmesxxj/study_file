from fastapi import APIRouter

'''
prefix
给整个路由加统一前缀
类似“分组路径”
tags
在 Swagger 文档中分组显示
非常重要API可读性
'''

shop2 = APIRouter(prefix="/shop1",tags=["购物车接口"])

@shop2.post("/cart")
def find_cart():
    return{"msg":"get cart"}

