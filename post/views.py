from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
from django.utils import timezone
from member.jwt_manager import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from member.models import Member
from keyword_.models import Keyword
import requests, json

def user_read(request):
    datas = {}
    if request.method == 'GET':
        results = Post.objects.all()
        post_num = 0
        for result in results:
            datas[post_num] = result.get_dic_for_user()
            post_num+= 1
        return JsonResponse(datas)
    return JsonResponse(datas)

def admin_read(request):
    datas = {}
    if request.method == 'GET':
        results = Post.objects.all()
        post_num = len(results)-1
        for result in results:
            datas[post_num] = result.get_dic_for_admin()
            post_num-=1
        return JsonResponse(datas)
    return JsonResponse(datas)

def user_post(request,pk) :
    if request.method == 'GET':
        post = Post.objects.get(post_id=pk)
        print(post.text)
        if(post == None):
            return_data = {'message' : '로그인 실패'}
            return JsonResponse(return_data, status=410)
        else :
            return JsonResponse(post.get_dic_for_user())



@csrf_exempt 
def user_search_post(request):
    try:
        datas ={}
        code = {'전체':0,'차가움':1,'따뜻함':2,'뜨거움':3,'제목':4,'내용':5,'필명':6,'키워드':7,'태그':8}
        if request.method == 'GET':
            search_code = int(request.GET.get('code'))
            query = request.GET.get('query')
            page_no = request.GET.get('page_no')
            print(search_code)
            if code['전체'] == search_code:
                result_posts = Post.objects.all()
                post_num = len(result_posts)-1
                for result in result_posts:
                    datas[post_num]=result.get_dic_for_user()
                    post_num-=1
                return JsonResponse(datas)
            elif code['차가움'] == search_code:
                cool_posts = Post.objects.filter(temperature__lt=32)
                post_num = 0
                for result in cool_posts:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
            elif code['따뜻함'] == search_code:
                warm_post = Post.objects.filter(temperature__range = (32.0 , 38.0))
                post_num = 0
                for result in warm_post:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
            elif code['뜨거움'] == search_code:
                hot_posts = Post.objects.filter(temperature__gt=38)
                post_num = 0
                for result in hot_posts:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
            elif code['제목'] == search_code:
                posts_title = Post.objects.filter(title__icontains=query)
                post_num = 0
                for result in posts_title:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
            elif code['내용'] == search_code:
                posts_text = Post.objects.filter(text__icontains=query)
                post_num = 0
                for result in posts_text:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
            elif code['필명'] == search_code:
                posts_writer = Post.objects.filter(writer__nickname__icontains= query)
                post_num = 0
                for result in posts_writer:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
            elif code['키워드'] == search_code:
                posts_keyword = Post.objects.filter(keyword__keyword__icontains = query)
                post_num = 0
                for result in posts_keyword:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
            elif code['태그'] == search_code:
                posts_tag = Post.objects.filter(tag__icontains = query)
                post_num = 0
                for result in posts_tag:
                    datas[post_num]=result.get_dic_for_user()
                    post_num+=1
                return JsonResponse(datas)
        if request.method == 'POST':
            p = json.loads(request.body.decode('utf-8'))
            member_info = get_member_info(request.COOKIES)
            print(member_info)
            tag = ""
            for x in p['tag']:
                tag+= (x + settings.TAG_SEPERATOR)
            member = Member.objects.get(id = member_info['id'])
            params = {'text': p['title'] + "\n" + p['text']}

            res = requests.get(settings.BERT_SERVER, params = params).json()
            prob_p_dp = res['result']['prob_p_dp']
            prob_a_da = res['result']['prob_a_da']
            prob_slang = res['result']['prob_slang']
            temperature = res['result']['temperature']
            
            try:
                keyword = Keyword.objects.get(keyword=p['keyword'])
                post = Post(title=p['title'], text=p['text'], tag=tag, writer=member, keyword=keyword, prob_p_dp=prob_p_dp, prob_a_da=prob_a_da, prob_is_slang=prob_slang, temperature=temperature)
                post.save()
            except :
                post = Post(title=p['title'], text=p['text'], tag=tag, writer=member, prob_p_dp=prob_p_dp, prob_a_da=prob_a_da, prob_is_slang=prob_slang, temperature=temperature)
                post.save()
            return JsonResponse({'message':'성공적으로 등록되었습니다.'},status=200)
    except Exception as e :
        print(e)
        return JsonResponse(datas, status=400)


# def admin_search_post(request):
#     try:
#         datas ={1:3}
#         code = {'전체':0,'차가움':1,'따뜻함':2,'제목':4,'내용':5,'작성자':6,'키워드':7,'태그':8}
#         search_criteria = json.loads(request.body.decode('utf-8'))
#         if request.method == 'GET':
#             search_code = search_criteria['code']
#             content = search_criteria['content']

#             if code['전체'] == search_code:
#                 posts_title = Post.objects.filter(title__icontains = content)
#                 posts_text = Post.objects.filter(text__icontains = content)
#                 posts_writer = Post.objects.filter(writer__icontains= content)
#                 posts_keyword = Post.objects.filter(keyword__icontains = content)
#                 posts_tag = Post.objects.filter(tag__icontains = content)

#                 #각 검색결과를 종합하는 함수
#                 result_posts = union(posts_title,posts_text,posts_writer,posts_keyword,posts_tag)
#                 post_num = 0
#                 for result in result_posts:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)

#             elif code['차가움'] == search_code:
#                 posts_title = Post.objects.filter(title__icontains=content)
#                 posts_text = Post.objects.filter(text__icontains=content)
#                 posts_writer = Post.objects.filter(writer__icontains= content)
#                 posts_keyword = Post.objects.filter(keyword__icontains = content)
#                 posts_tag = Post.objects.filter(tag__icontains = content)
#                 result_all_posts = union(posts_title,posts_text,posts_writer,posts_keyword,posts_tag)
                
#                 # 34도 미만의 게시글을 차가움이라 가정
#                 cool_posts = Post.objects.filter(temperature__lt=34)

#                 # 차가움과 검색결과의 포스터 교집합을 결과로 한다.
#                 result_posts = intersection(result_all_posts,cool_posts)
#                 post_num = 0
#                 for result in result_posts:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)

#             elif code['따뜻함'] == search_code:
#                 posts_title = Post.objects.filter(title__icontains=content)
#                 posts_text = Post.objects.filter(text__icontains=content)
#                 posts_writer = Post.objects.filter(writer__icontains= content)
#                 posts_keyword = Post.objects.filter(keyword__icontains = content)
#                 posts_tag = Post.objects.filter(tag__icontains = content)
#                 result_all_posts = union(posts_title,posts_text,posts_writer,posts_keyword,posts_tag)
                
#                 # 37도 초과의 게시글을 따뜻함이라 가정
#                 cool_posts = Post.objects.filter(temperature__gt=37)
                
#                 # 따뜻함과 검색결과의 포스터 교집합을 결과로 한다.
#                 result_posts = intersection(result_all_posts,cool_posts)
#                 post_num = 0
#                 for result in result_posts:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)

#             elif code['제목'] == search_code:
#                 posts_title = Post.objects.filter(title__icontains=content)
#                 post_num = 0
#                 for result in posts_title:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)
#             elif code['내용'] == search_code:
#                 posts_text = Post.objects.filter(text__icontains=content)
#                 post_num = 0
#                 for result in posts_text:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)

#             elif code['작성자'] == search_code:
#                 posts_writer = Post.objects.filter(writer__icontains= content)
#                 post_num = 0
#                 for result in posts_writer:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)

#             elif code['키워드'] == search_code:
#                 posts_keyword = Post.objects.filter(keyword__icontains = content)
#                 post_num = 0
#                 for result in posts_keyword:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)

#             elif code['태그'] == search_code:
#                 posts_tag = Post.objects.filter(tag__icontains = content)
#                 post_num = 0
#                 for result in posts_tag:
#                     datas[post_num]=result.get_dic_for_admin()
#                     post_num+=1
#                 return JsonResponse(datas)
#     except Exception as e :
#         return JsonResponse(status=410)

