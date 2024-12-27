import json
from loguru import logger
from robyn.types import PathParams
from robyn import SubRouter, Request
from utils.reqmodel import BlogGetSingleResponse, GeneralResponse
from crud.blog import db_get_blog_single, db_create_blog, db_get_blog_list_by_condition, db_update_blog, db_delete_blog

api_blog = SubRouter(__name__, prefix="/api/blog")

@api_blog.get("/getblog/:id", openapi_name="查询单个博客")
def get_blog_single(request: PathParams) -> BlogGetSingleResponse:
    try:
        res = db_get_blog_single(request['id'])
        data = {"id": res.id, "title": res.title, "content": res.content}
        return {'code': 0, 'status': 'success', 'msg': "查询成功", 'data': data}
    except Exception as e:
        return {'code': -1, 'status': 'error', 'msg': "查询失败", 'data': {}}

@api_blog.post("/getblog", openapi_name="分页查询博客")
async def get_blog(request: Request) -> BlogGetSingleResponse:
    req = json.loads(request.body)
    try:
        res, count = db_get_blog_list_by_condition(req['page'], req['size'], req['search'])
        data = {
            'data': [{"id": it.id, "title": it.title, "content": it.content, 'created_at':it.created_at, 'updated_at': it.updated_at} for it in res],
            'count': count
        }
        return {'code': 0, 'status': 'success', 'msg': "查询成功", 'data': data}
    except Exception as e:
        return {'code': -1, 'status': 'error', 'msg': "查询失败", 'data': {}}

@api_blog.post("/createblog", openapi_name="创建博客")
async def create_blog(request: Request) -> GeneralResponse:
    req = json.loads(request.body)
    try:
        db_create_blog(req['title'], req['content'])
        return {'code': 0, 'status': 'success', 'msg': "创建成功"}
    except Exception as e:
        return {'code': -1, 'status': 'error', 'msg': "创建失败"}

@api_blog.post("/updateblog", openapi_name="更新博客")
async def update_blog(request: Request):
    body = json.loads(request.body)
    try:
        db_update_blog(body['id'], body['title'], body['content'])
        return {'code': 0, 'status': 'success', 'msg': "更新成功"}
    except Exception as e:
        return {'code': -1, 'status': 'error', 'msg': "更新失败"}

@api_blog.post("/deleteblog", openapi_name="删除博客")
async def delete_blog(request: Request):
    body = json.loads(request.body)
    try:
        db_delete_blog(body['id'])
        return {'code': 0, 'status': 'success', 'msg': "删除成功"}
    except Exception as e:
        return {'code': -1, 'status': 'error', 'msg': "删除失败"}