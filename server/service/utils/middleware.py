from service.models import User
from django.http import JsonResponse

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object

# 白名单，表示请求里面的路由时不验证登录信息
API_WHITELIST = ["/login/"]


class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in API_WHITELIST:
            pass
        else:
            if User.objects.filter(access_token=request.META.get("HTTP_AUTHORIZATION")).exists() == False:
                return JsonResponse({"code": -2, "msg": "未查询到登录信息"})