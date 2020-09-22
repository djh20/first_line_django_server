from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def readAll(request):
    datas = {}
    if request.method == 'GET':
        results = Post.objects.all()
        post_num = 0
        for result in results:
            datas[post_num] = {'title' : result.title, 'content' : result.content}
            post_num+= 1
        print(datas)
        return JsonResponse(datas)
    return JsonResponse(datas)

