import json
import requests
from datetime import datetime
from django.db.models import Q
from server.settings import CONFIG
from easydict import EasyDict as ed
from django.http import JsonResponse
from service.models import User, Notes
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = ed(json.loads(request.body))
        try:
            username = data.username.strip()
            password = data.password.strip()
        except:
            return JsonResponse({"code": -1, "data": "参数有误"})
        try:
            res = ed(requests.post("https://gitee.com/oauth/token", {'grant_type': 'password', 'username': username,'password': password,'client_id': CONFIG['gitee_app_client_id'],'client_secret': CONFIG['gitee_app_client_secret'], 'scope': 'user_info emails'}).json())
            user_info = ed(requests.get(f"https://gitee.com/api/v5/user?access_token={res.access_token}").json())
            data_info = {
                "user_id": user_info.id,
                "name": user_info.name,
                "avatar_url": user_info.avatar_url,
                "email": user_info.email,
                "access_token": res.access_token,
                "refresh_token": res.refresh_token,
                "expires_in": res.expires_in,
                "created_at": res.created_at
            }

            if User.objects.filter(user_id=data_info['user_id']).exists():
                User.objects.filter(user_id=data_info['user_id']).update(**data_info)
            else:
                User.objects.create(**data_info)
            return JsonResponse({"code": 0, "msg": "登录成功", "data": data_info})
        except:
            return JsonResponse({"code": -1, "data": "用户名或密码错误"})

@csrf_exempt
def article(request):
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            article_id_info = Notes.objects.get(id = id)
            return JsonResponse({"code": 0, "data": {"id": article_id_info.id, "title": article_id_info.title, "article": article_id_info.article, 'avatar': article_id_info.user.avatar_url}})
        except:
            return JsonResponse({"code": -1, "data": "没有找到相关数据喔 ~"})
    if request.method == "POST":
        page_data = ed(json.loads(request.body))
        try:
            data = {"user": User.objects.get(id=User.objects.get(user_id=page_data.user_id).id),"title": page_data.title, "article": page_data.article}
        except:
            return JsonResponse({"code": -1, "data": "参数有误"})
        try:
            Notes.objects.create(**data)
            return JsonResponse({"code": 0, "data": "添加成功"})
        except:
            return JsonResponse({"code": -1, "data": "哎呦, 出错了呢"})
    if request.method == "PUT":
        page_data = ed(json.loads(request.body))
        id = page_data.id
        data = {"title": page_data.title, "article": page_data.article, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        try:
            Notes.objects.filter(id=id).update(**data)
            return JsonResponse({"code": 0, "data": "修改成功"})
        except:
            return JsonResponse({"code": -1, "data": "哎呦, 出错了呢"})

@csrf_exempt
def article_delete(request):
    if request.method == "POST":
        try:
            id = ed(json.loads(request.body)).id
            Notes.objects.get(id=id).delete()
            return JsonResponse({"code": 0, "data": "删除成功"})
        except:
            return JsonResponse({"code": -1, "data": "删除错误"})

@csrf_exempt
def article_search(request):
    if request.method == "POST":
        page_data = ed(json.loads(request.body))
        try:
            question = page_data.question
            page_index = page_data.page_index
            page_size = page_data.page_size
        except:
            return JsonResponse({"code": -1, "data": "参数有误"})

        query_model = Notes.objects.all().order_by("created_at")
        article_count = query_model.count()

        if question.strip() != "":
            query = Q(title__contains=question) | Q(article__contains=question)
            query_model = Notes.objects.filter(query)

        pageInator = Paginator(query_model, page_size)
        
        try:
            context = pageInator.page(page_index)
        except EmptyPage:
            context = pageInator.page((query_model.count()//page_size) + 1)
        data = [{"id": it.id, "title": it.title, "article": it.article, 'avatar': it.user.avatar_url, 'created_at': it.created_at.strftime("%Y-%m-%d %H:%M:%S"), 'updated_at': it.updated_at.strftime("%Y-%m-%d %H:%M:%S")} for it in context]
        return JsonResponse({"code": 0, "article_count": article_count,"count": query_model.count(), "data": data})
