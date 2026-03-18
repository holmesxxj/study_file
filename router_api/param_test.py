from fastapi import APIRouter, Path, Query

post_param = APIRouter(prefix="/param",tags=["路由传参测试"])



'''
预设值传参
'''
from enum import Enum

class EmpName(str, Enum):
    zs = '张三'
    ls = '李四'
    ww = '王五'

@post_param.put('/emp/{emp_name}')
def update_emp(emp_name: EmpName):
    return {"emp_value": emp_name.value}

'''
URL 传参分两种：

/path/{xxx} → 路径参数（必须）

?a=1&b=2 → 查询参数（可选）
'''
# request_url http://127.0.0.1:8000/param/query/?q=aa&page=1
@post_param.get("/query/")
def read_items(q: str = None, page: int = 1):
    return {"q": q,"page":page}

@post_param.get("/p/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

'''
路由的映射：
    请求的路径
    请求的方法
    对应的函数
'''
#get("/p/all") 会和get("/p/{item_id}") 冲突
@post_param.get("/p/all")
def get_item_all(item_id: int):
    return {"item_id": item_id}


#delete("/p/all")不 会和get("/p/{item_id}") 冲突
@post_param.delete("/p/all")
def get_item_all(item_id: int):
    return {"item_id": item_id}



'''
参数校验
'''
@post_param.get("/validate/{item_id}")
def validate_params(
    item_id: int = Path(..., ge=1, le=10000, description="item_id 范围 1-10000"),
    keyword: str = Query(
        ...,
        min_length=2,
        max_length=20,
        pattern="^[a-zA-Z0-9_]+$",
        description="keyword 仅允许字母、数字、下划线",
    ),
    page: int = Query(1, ge=1, le=100, description="page 范围 1-100"),
):
    return {"item_id": item_id, "keyword": keyword, "page": page}



