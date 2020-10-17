from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
from django.utils import timezone

def readAll(request):
    datas = {}
    print(timezone.now(), "dasd")
    if request.method == 'GET':
        results = Post.objects.all()
        post_num = 0
        for result in results:
            datas[post_num] = result.get_dic_for_user()
            post_num+= 1
        return JsonResponse(datas)
    return JsonResponse(datas)

