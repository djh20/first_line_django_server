from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
from django.utils import timezone

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
        post_num = 0
        for result in results:
            datas[post_num] = result.get_dic_for_admin()
            post_num+= 1
        return JsonResponse(datas)
    return JsonResponse(datas)

def user_post(request,pk) :
    if request.method == 'GET':
        post = Post.objects.get(post_id=pk)
        if(post == None):
            return_data = {'message' : '로그인 실패'}
            return JsonResponse(return_data, status=410)
        else :
            return JsonResponse(post.get_dic_for_user())


def search_post(request):
    datas ={}
    code = {'전체':0,'차가움':1,'따뜻함':2,'제목':4,'내용':5,'작성자':6,'키워드':7,'태그':8}
    search_criteria = json.loads(request.body.decode('utf-8'))
    if request.method == 'GET':
        search_code = search_criteria['code']
        content = search_criteria['content']

        if code['전체'] == search_code:
            posts_title = Post.filter(title__icontains = content)
            posts_text = Post.filter(text__icontains = content)
            posts_writer = Post.filter(writer__icontains= content)
            posts_keyword = Post.filter(keyword__icontains = content)
            posts_tag = Post.filter(tag__icontains = content)
            
            #각 검색결과를 종합하는 함수
            result_posts = union(posts_title,posts_text,posts_writer,posts_keyword,posts_tag)
            post_num = 0
            for result in result_posts:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)

        elif code['차가움'] == search_code:
            posts_title = Post.filter(title__icontains=content)
            posts_text = Post.filter(text__icontains=content)
            posts_writer = Post.filter(writer__icontains= content)
            posts_keyword = Post.filter(keyword__icontains = content)
            posts_tag = Post.filter(tag__icontains = content)
            result_all_posts = union(posts_title,posts_text,posts_writer,posts_keyword,posts_tag)
            
            # 34도 미만의 게시글을 차가움이라 가정
            cool_posts = Post.filter(temperature__lt=34)

            # 차가움과 검색결과의 포스터 교집합을 결과로 한다.
            result_posts = intersection(result_all_posts,cool_posts)
            post_num = 0
            for result in result_posts:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)

        elif code['따뜻함'] == search_code:
            posts_title = Post.filter(title__icontains=content)
            posts_text = Post.filter(text__icontains=content)
            posts_writer = Post.filter(writer__icontains= content)
            posts_keyword = Post.filter(keyword__icontains = content)
            posts_tag = Post.filter(tag__icontains = content)
            result_all_posts = union(posts_title,posts_text,posts_writer,posts_keyword,posts_tag)
            
            # 37도 초과의 게시글을 따뜻함이라 가정
            cool_posts = Post.filter(temperature__gt=37)
            
            # 따뜻함과 검색결과의 포스터 교집합을 결과로 한다.
            result_posts = intersection(result_all_posts,cool_posts)
            post_num = 0
            for result in result_posts:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)

        elif code['제목'] == search_code:
            posts_title = Post.filter(title__icontains=content)
            post_num = 0
            for result in posts_title:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)
        elif code['내용'] == search_code:
            posts_text = Post.filter(text__icontains=content)
            post_num = 0
            for result in posts_text:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)

        elif code['작성자'] == search_code:
            posts_writer = Post.filter(writer__icontains= content)
            post_num = 0
            for result in posts_writer:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)

        elif code['키워드'] == search_code:
            posts_keyword = Post.filter(keyword__icontains = content)
            post_num = 0
            for result in posts_keyword:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)

        elif code['태그'] == search_code:
            posts_tag = Post.filter(tag__icontains = content)
            post_num = 0
            for result in posts_tag:
                datas[post_num]=result.get_dic_for_user()
                post_num+=1
            return JsonResponse(datas)
    return JsonResponse(datas)


