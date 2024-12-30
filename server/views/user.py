import json
from crud.user import *
from robyn import SubRouter, Request
from utils.password import gen_password
from utils.token import create_access_token
from utils.reqmodel import LoginResponse, GeneralResponse

api_auth = SubRouter(__name__, prefix="/api/auth")


@api_auth.post("/login", openapi_name="登录")
async def login(request: Request) -> LoginResponse:
    req = json.loads(request.body)
    flag,msg,md = await db_login(req['username'], req['password'])
    token = await create_access_token({"username": req['username']})
    if flag:
        data = {'id': md.id, 'username': md.username, 'avatar': md.avatar, 'created_at': md.created_at.strftime("%Y-%m-%d %H:%M:%S"), 'updated_at': md.updated_at.strftime("%Y-%m-%d %H:%M:%S"), 'token': token}
        return {'code': 0, 'status': 'success', 'msg': msg, 'data': data}
    else: return {'code': -1, 'status': 'error', 'msg': msg, 'data': {}}

@api_auth.post("/register", openapi_name="注册")
async def register(request: Request) -> GeneralResponse:
    data = json.loads(request.body)
    flag,msg = await db_register(data['username'], gen_password(data['password']))
    
    if flag: return {'code': 0, 'status': 'success', 'msg': msg}
    else: return {'code': -1, 'status': 'error', 'msg': msg}

# def get_user(request):
#     pass

# async def update_user_password(request):
#     pass

@api_auth.post("/update/avatar", openapi_name="更新头像")
async def update_user_avatar(request: Request) -> GeneralResponse:
    req = json.loads(request.body)
    try:
        db_update_avatar(req['id'], req['avatar'])
        return {'code': 0, 'status': 'success', 'msg': "更新成功"}
    except Exception as e:
        return {'code': -1, 'status': 'error', 'msg': "更新失败"}