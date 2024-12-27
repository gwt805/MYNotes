from views.user import api_auth
from views.file import api_file
from views.blog import api_blog
from utils.middleware import request_before
from robyn import Robyn, ALLOW_CORS, Response, Request
from robyn.openapi import OpenAPI, OpenAPIInfo,Components,Contact,ExternalDocumentation

app = Robyn(file_object=__file__,openapi=OpenAPI(info=OpenAPIInfo(
    title="Blog OpenAPI Docs",
    description="博客服务应用.",
    version="1.0.0",
    contact=Contact(
        name="API Support",
        url="http://localhost:5174",
        email="1973735972@qq.com",
    ),
    externalDocs=ExternalDocumentation(description="Find more info here", url=""),
    components=Components(),
)))

ALLOW_CORS(app=app, origins=["*"])

app.include_router(api_auth)
app.include_router(api_file)
app.include_router(api_blog)

@app.before_request()
async def hello_before_request(request:Request):
    import json
    skip_router = ['/api/auth/login', '/api/auth/register', '/docs', '/openapi.json']
    if request.url.path not in skip_router:
        try:
            flag, data = await request_before(request.headers["Authorization"])
            if not flag:
                return Response(status_code=401,headers= request.headers,description=json.dumps(data))
            else: return request
        except:
            return Response(status_code=401,headers= request.headers,description=json.dumps({"code": -2, "status": "error", "msg": "请先登录"}))
    else: return request

if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8000)
