from django.shortcuts import render
from .models import Reply
import json
from django.http import JsonResponse
from member.jwt_manager import get_member_info
from django.views.decorators.csrf import csrf_exempt
from post.models import Post
from member.models import Member
import requests, json
from django.conf import settings


@csrf_exempt 
def admin_reply(request):
    if request.method == 'GET':
        replies = Reply.objects.all()
        data = {}
        reply_num = len(replies)-1
        for reply in replies:
            data[reply_num] = reply.get_dic_for_admin()
            reply_num-=1
        return JsonResponse(data)

# Create your views here.
@csrf_exempt 
def user_reply(request):
    if request.method == "GET":
        if request.GET.get('post_id') != None:
            try:
                replies = Reply.objects.filter(post_id=request.GET.get('post_id'))
                data = {}
                reply_num = 0
                for reply in replies:
                    data[reply_num] = reply.get_dic_for_user()
                    reply_num+=1
                
                return JsonResponse(data)
            except Exception as e:
                print(e)
                return JsonResponse({'message':"댓글 없음"}, status=410)
    if request.method == "POST":
        member_info = get_member_info(request.COOKIES)
        if member_info != None:
            try:
                print(member_info)
                reply_info = json.loads(request.body.decode('utf-8'))
                member = Member.objects.get(id = member_info['id'])
                post = Post.objects.get(post_id=int(reply_info['post_id']))

                params = {'text': reply_info['text']}
                res = requests.get(settings.BERT_SERVER, params = params).json()
                prob_p_dp = res['result']['prob_p_dp']
                prob_a_da = res['result']['prob_a_da']
                prob_slang = res['result']['prob_slang']
                temperature = res['result']['temperature']

                reply = Reply(post_id = post, writer = member,text = reply_info['text'], prob_is_slang=prob_slang)
                reply.save()
                return JsonResponse({'message':"등록 성공"}, status=200)
            except Exception as e:
                print(e)
        else:
            return JsonResponse({'message':"등록 실패"}, status=410)
        