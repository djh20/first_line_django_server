from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
from .models import LikeRecord, LookupRecord
from django.utils import timezone
from member.jwt_manager import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from member.models import Member, SementicRecord
from keyword_.models import Keyword
from notice.views import process_create_notice
import json
import datetime
from urllib import parse

# 사용자의 게시글 관련 요청 처리 함수
@csrf_exempt 
def user_process_post(request):
    if request.method == 'GET':
        # Read 작업 - 게시글 조회(사용자) - 특정 게시글의 경우 따로 접근
        return user_search_post(request)


    elif request.method == 'POST':
        # Create 작업 - 게시글 등록(사용자)
        post_info = json.loads(request.body.decode('utf-8'))
        member_info = get_member_info(request.COOKIES)
        return write_post(member_info,post_info)

    elif request.method == 'PUT':
        # Update 작업 - 게시글 수정(사용자)
        post_info = json.loads(request.body.decode('utf-8'))
        member_info = get_member_info(request.COOKIES)
        return user_update_post(member_info,post_info)

    else :
        # Delete 작업 - 게시글 삭제(사용자) 
        post_info = json.loads(request.body.decode('utf-8'))
        member_info = get_member_info(request.COOKIES)
        return user_delete_post(member_info,post_info)


# 관리자의 게시글 관련 요청 처리 함수
@csrf_exempt 
def admin_process_post(request):
    if request.method == 'GET':
        # Read 작업 - 게시글 조회(관리자)
        if request.GET.get('code') != None:
            return admin_search_post(request)
        else:
            return admin_read_all_post(request)

    elif request.method == 'POST':
        # Create 작업 - 게시글 등록(관리자)
        post_info = json.loads(request.body.decode('utf-8'))
        member_info = get_member_info(request.COOKIES)
        return write_post(member_info,post_info)

    elif request.method == 'PUT':
        # Update 작업 - 게시글 수정(관리자)
        post_info = json.loads(request.body.decode('utf-8'))
        member_info = get_member_info(request.COOKIES)
        return admin_update_post(member_info,post_info)

    else :
        # Delete 작업 - 게시글 삭제(관리자)
        posts = json.loads(request.body.decode('utf-8'))
        posts = posts['post']
        posts = posts['rows']
        return admin_delete_post(posts)



# ==================================================================================================================================
#                                               게시글 검색 함수 모음
# ==================================================================================================================================

# 사용자 게시글 검색 함수
@csrf_exempt 
def user_search_post(request):
    try:
        # GET method로 요청할 시 - 검색
        if request.method == 'GET':
            search_code = int(request.GET.get('code'))
            query = request.GET.get('query')
            # 검색 작업 수행
            return search_post(search_code,query,False)
    except Exception as e :
        print(e)
        datas = {'message' : '오류가 발생했습니다.'}
        return JsonResponse(datas, status=400)


# 관리자 게시글 검색 함수
@csrf_exempt
def admin_search_post(request):
    try:
        # GET method로 요청할 시 - 검색
        if request.method == 'GET':
            search_code = int(request.GET.get('code'))
            query = parse.unquote(request.GET.get('query'))
            # 검색 작업 수행
            return search_post(search_code,query,True)         
    except Exception as e :
        print(e)
        datas = {'message' : '오류가 발생했습니다.'}
        return JsonResponse(datas, status=400)


# 게시글 검색 함수
def search_post(search_code,query,isAdmin):
    if query == '':
        datas = search_post_entire(isAdmin)
        return JsonResponse(datas, status=200)
        
    code = {'전체':0,'차가움':1,'따뜻함':2,'뜨거움':3,'제목':4,'게시글 번호(이상)':5,'게시글 번호(이하)':6,
    '조회수(이상)':7,'조회수(이하)':8,'좋아요(이상)':9 , '좋아요(이하)':10, '댓글 수(이상)':11, '댓글 수(이하)':12,
    '태그':13, '작성자':14, '작성일(이후)':15, '작성일(이전)':16, '수정일(이후)':17, '수정일(이전)':18,
    '온도(이상)': 19, '온도(이하)':20, '키워드':21, 'P/DP(이상)':22, 'P/DP(이하)':23, 'A/DA(이상)':24,
    'A/DA(이하)':25, '욕설확률(이상)':26, '욕설확률(이하)':27, '삭제여부':28, '블라인드 여부':29,'내용':30}

    if code['전체'] == search_code:
        datas = search_post_entire(isAdmin)
        return JsonResponse(datas, status=200)

    elif code['차가움'] == search_code:
        datas = search_post_cold(isAdmin)
        return JsonResponse(datas, status=200)

    elif code['따뜻함'] == search_code:
        datas = search_post_warm(isAdmin)
        return JsonResponse(datas, status=200)

    elif code['뜨거움'] == search_code:
        datas = search_post_hot(isAdmin)
        return JsonResponse(datas, status=200)

    elif code['제목'] == search_code:
        datas = search_post_title(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['게시글 번호(이상)'] == search_code:
        datas = search_post_num_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['게시글 번호(이하)'] == search_code:
        datas = search_post_num_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['조회수(이상)'] == search_code:
        datas = search_post_num_lookup_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['조회수(이하)'] == search_code:
        datas = search_post_num_lookup_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['좋아요(이상)'] == search_code:
        datas = search_post_num_good_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['좋아요(이하)'] == search_code:
        datas = search_post_num_good_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['댓글 수(이상)'] == search_code:
        datas = search_post_num_reply_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['댓글 수(이하)'] == search_code:
        datas = search_post_num_reply_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['태그'] == search_code:
        datas = search_post_tag(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['작성자'] == search_code:
        datas = search_post_writer(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['작성일(이후)'] == search_code:
        datas = search_post_writing_date_after(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['작성일(이전)'] == search_code:
        datas = search_post_writing_date_before(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['수정일(이후)'] == search_code:
        datas = search_post_editing_date_after(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['수정일(이전)'] == search_code:
        datas = search_post_editing_date_before(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['온도(이상)'] == search_code:
        datas = search_post_temperature_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['온도(이하)'] == search_code:
        datas = search_post_temperature_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['키워드'] == search_code:
        datas = search_post_keyword(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['P/DP(이상)'] == search_code:
        datas = search_post_P_DP_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['P/DP(이하)'] == search_code:
        datas = search_post_P_DP_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['A/DA(이상)'] == search_code:
        datas = search_post_A_DA_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['A/DA(이하)'] == search_code:
        datas = search_post_A_DA_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['욕설확률(이상)'] == search_code:
        datas = search_post_slang_over(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['욕설확률(이하)'] == search_code:
        datas = search_post_slang_under(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['삭제여부'] == search_code:
        datas = search_post_is_deleted(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['블라인드 여부'] == search_code:
        datas = search_post_is_blinded(query,isAdmin)
        return JsonResponse(datas, status=200)

    elif code['내용'] == search_code:
        datas = search_post_text(query,isAdmin)
        return JsonResponse(datas, status=200)

    

    

    



def search_post_entire(isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.all()
    else:
        result_posts = Post.objects.filter(is_deleted = False , is_blinded = False)
    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1

    return datas


def search_post_cold(isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 온도 조절이 필요함 (32도보다 낮은경우가 적음)
    if isAdmin:
        result_posts = Post.objects.filter(temperature__lt=32)
    else:
        result_posts = Post.objects.filter(temperature__lt=32, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_warm(isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.filter(temperature__range = (32.0 , 38.0))
    else:
        result_posts = Post.objects.filter(temperature__range = (32.0 , 38.0), is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_hot(isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.filter(temperature__gt=38)
    else:
        result_posts = Post.objects.filter(temperature__gt=38, is_deleted = False , is_blinded = False)
    
    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_title(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.filter(title__contains=query)
    else:
        result_posts = Post.objects.filter(title__contains=query, is_deleted = False , is_blinded = False)
    
    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas



def search_post_num_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(post_id__gte=query)
    else:
        result_posts = Post.objects.filter(post_id__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_num_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(post_id__lte=query)
    else:
        result_posts = Post.objects.filter(post_id__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_num_lookup_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(num_lookup__gte=query)
    else:
        result_posts = Post.objects.filter(num_lookup__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_num_lookup_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(num_lookup__lte=query)
    else:
        result_posts = Post.objects.filter(num_lookup__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_num_good_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(num_good__gte=query)
    else:
        result_posts = Post.objects.filter(num_good__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_num_like_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(num_good__lte=query)
    else:
        result_posts = Post.objects.filter(num_good__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_num_reply_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(num_reply__gte=query)
    else:
        result_posts = Post.objects.filter(num_reply__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_num_reply_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(num_reply__lte=query)
    else:
        result_posts = Post.objects.filter(num_reply__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_tag(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.filter(tag__icontains = query)
    else:
        result_posts = Post.objects.filter(tag__icontains = query, is_deleted = False , is_blinded = False)
    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_writer(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.filter(writer__nickname__icontains= query)
    else:
        result_posts = Post.objects.filter(writer__nickname__icontains= query, is_deleted = False , is_blinded = False)
    
    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas


def search_post_writing_date_after(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(writing_date__gte=query)
    else:
        result_posts = Post.objects.filter(writing_date__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_writing_date_before(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(writing_date__lte=query)
    else:
        result_posts = Post.objects.filter(writing_date__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_editing_date_after(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(editing_date__gte=query)
    else:
        result_posts = Post.objects.filter(editing_date__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_editing_date_before(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(editing_date__lte=query)
    else:
        result_posts = Post.objects.filter(editing_date__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_temperature_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(temperature__gte=query)
    else:
        result_posts = Post.objects.filter(temperature__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_temperature_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(temperature__lte=query)
    else:
        result_posts = Post.objects.filter(temperature__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas


def search_post_keyword(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.filter(keyword__keyword__icontains = query)
    else:
        result_posts = Post.objects.filter(keyword__keyword__icontains = query, is_deleted = False , is_blinded = False)
    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas


def search_post_P_DP_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(prob_p_dp__gte=query)
    else:
        result_posts = Post.objects.filter(prob_p_dp__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_P_DP_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(prob_p_dp__lte=query)
    else:
        result_posts = Post.objects.filter(prob_p_dp__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_A_DA_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(prob_a_da__gte=query)
    else:
        result_posts = Post.objects.filter(prob_a_da__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_A_DA_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(prob_a_da__lte=query)
    else:
        result_posts = Post.objects.filter(prob_a_da__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_slang_over(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(prob_is_slang__gte=query)
    else:
        result_posts = Post.objects.filter(prob_is_slang__gte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_slang_under(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 - 
    if isAdmin:
        result_posts = Post.objects.filter(prob_is_slang__lte=query)
    else:
        result_posts = Post.objects.filter(prob_is_slang__lte=query, is_deleted = False , is_blinded = False)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

def search_post_is_deleted(query):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능 
    result_posts = Post.objects.filter(is_deleted=query)
    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(True)
        post_num-=1
    return datas

def search_post_is_blinded(query):
    datas ={}
    result_posts = Post.objects.filter(is_blinded=query)

    post_num = len(result_posts)-1
    for result in result_posts:
        datas[post_num]=result.get_dic(True)
        post_num-=1
    return datas

def search_post_text(query,isAdmin):
    datas ={}
    # 관리자인 경우 blind나 삭제된 게시글을 조회 가능
    if isAdmin:
        result_posts = Post.objects.filter(text__contains=query)
    else:
        result_posts = Post.objects.filter(text__contains=query, is_deleted = False , is_blinded = False)
    post_num = len(result_posts)-1
    print(post_num)
    for result in result_posts:
        datas[post_num]=result.get_dic(isAdmin)
        post_num-=1
    return datas

# ==================================================================================================================================
#                                               게시글 등록 관련 함수
# ==================================================================================================================================

def write_post(memberInfo, postInfo):
    # 게시글에 대한 검증 작업
    if not isValid_text_length(postInfo['text']):
        return JsonResponse({'message':'글의 내용이 너무 깁니다.\n3000자 제한'},status=453)

    if not isValid_title_length(postInfo['title']):
        return JsonResponse({'message':'제목이 너무 깁니다.\n30자 제한'},status=452)

    # 태그 문자열로 변환
    tag = ""
    for x in postInfo['tag']:
        tag+= (x + settings.TAG_SEPERATOR)

    # 회원 객체 불러오기 - 작성자 등록
    member = Member.objects.get(id = memberInfo['id'])

    # 긍/부정, 격렬/차분, 비속어 확률과 글의 온도 획득
    params = {'text': postInfo['title'] + "\n" + postInfo['text']}

    res = requests.get(settings.BERT_SERVER, params = params).json()
    prob_p_dp = res['result']['prob_p_dp']
    prob_a_da = res['result']['prob_a_da']
    prob_slang = res['result']['prob_slang']
    temperature = res['result']['temperature']
            
    # 게시글 등록
    try:
        # 키워드를 사용한 경우
        keyword = Keyword.objects.get(keyword=postInfo['keyword'])
        post = Post(title=postInfo['title'], text=postInfo['text'], tag=tag, writer=member, keyword=keyword, prob_p_dp=prob_p_dp, prob_a_da=prob_a_da, prob_is_slang=prob_slang, temperature=temperature)
        post.save()
    except:
        # 키워드를 사용하지 않은 경우
        post = Post(title=postInfo['title'], text=postInfo['text'], tag=tag, writer=member, prob_p_dp=prob_p_dp, prob_a_da=prob_a_da, prob_is_slang=prob_slang, temperature=temperature)
        post.save()
    return JsonResponse({'message':'성공적으로 등록되었습니다.'},status=200)


# ==================================================================================================================================
#                                               게시글 조회 관련 함수
# ==================================================================================================================================

# 사용자가 볼 수 있는 모든 게시글을 조회한다
def user_read_all_post(request):
    datas = {}
    if request.method == 'GET':
        results = Post.objects.filter(is_blinded = False, is_deleted = False)
        post_num = len(results)-1
        for result in results:
            datas[post_num] = result.get_dic(False)
            post_num-= 1
        return JsonResponse(datas)
    return JsonResponse({'message':'잘못된 요청 메소드'},status = 490)


# 특정 게시글을 조회한다 - 조회 기록 남기기
@csrf_exempt
def user_read_post(request,pk) :
    if request.method == 'GET':
        post = Post.objects.get(post_id=pk)
        # 조회수 증가
        post.num_lookup = post.num_lookup +1
        post.save()

        # 조회 기록 남기기 - 여러번 방문했을 경우에도 한번만 방문기록을 남김
        member_info = get_member_info(request.COOKIES)
        member = Member.objects.get(id=member_info['id'])
        
        if not LookupRecord.objects.filter(member_id=member,post_id=post).exists():
            lookup_record = LookupRecord(member_id=member,post_id=post,temperature=post.temperature,is_like=False)
            lookup_record.save()
            # 감정지수 남기기
            sementic_record = SementicRecord.objects.get(date = datetime.date.today() ,member = member)
            sementic_record.current_temperature = ((sementic_record.current_temperature*sementic_record.reflected_number) + post.temperature)/(sementic_record.reflected_number + 1)
            sementic_record.reflected_number = sementic_record.reflected_number + 1
            sementic_record.save()


        if(post == None):
            return_data = {'message' : '해당 게시글이 존재하지 않습니다.'}
            return JsonResponse(return_data, status=454)
        # 삭제처리된 게시글인 경우
        elif post.is_deleted == True:
            return_data = {'message' : '해당 게시글이 존재하지 않습니다.'}
            return JsonResponse(return_data, status=454)
        else :
            # 글을 조회하는 사용자가 작성자인지 확인
            memberInfo = get_member_info(request.COOKIES)
            member = Member.objects.get(id = memberInfo['id'])
            
            return JsonResponse(post.get_dic(False))
            
            # Front 측에서 아래의 형식을 받도록 수정해야 함
            if post.writer.id == member.id:
                return_data = {'post':post.get_dic(False), 'isMyPost': True}
            else:
                return_data = {'post':post.get_dic(False), 'isMyPost': False}
            return JsonResponse(return_data)


def admin_read_all_post(request):
    datas = {}
    if request.method == 'GET':
        results = Post.objects.all()
        post_num = len(results)-1
        for result in results:
            datas[post_num] = result.get_dic(True)
            post_num-=1
        return JsonResponse(datas)
    return JsonResponse(datas)



# ==================================================================================================================================
#                                               게시글 수정 관련 함수
# ==================================================================================================================================

# 사용자가 게시글을 수정하는 함수
def user_update_post(memberInfo, postInfo):
    member_id = memberInfo['id']
    post_id = postInfo['id']

    if isValid_access_post(member_id,post_id):
        # 게시글에 대한 검증 작업
        if not isValid_text_length(postInfo['text']):
            return JsonResponse({'message':'글의 내용이 너무 깁니다.\n3000자 제한'},status=453)

        if not isValid_title_length(postInfo['title']):
            return JsonResponse({'message':'제목이 너무 깁니다.\n30자 제한'},status=452)
        
        # 태그 문자열로 변환
        tag = ""
        for x in postInfo['tag']:
            tag+= (x + settings.TAG_SEPERATOR)

        # 회원 객체 불러오기 - 작성자 등록
        member = Member.objects.get(id = memberInfo['id'])

        # 긍/부정, 격렬/차분, 비속어 확률과 글의 온도 획득
        params = {'text': postInfo['title'] + "\n" + postInfo['text']}

        res = requests.get(settings.BERT_SERVER, params = params).json()
        prob_p_dp = res['result']['prob_p_dp']
        prob_a_da = res['result']['prob_a_da']
        prob_slang = res['result']['prob_slang']
        temperature = res['result']['temperature']

        # 수정할 post 읽어오기
        post = Post.objects.get(post_id = post_id)
        post.title = postInfo['title']
        post.text=postInfo['text']
        post.tag=tag
        post.writer=member
        post.prob_p_dp=prob_p_dp
        post.prob_a_da=prob_a_da
        post.prob_is_slang=prob_slang
        post.temperature=temperature
        post.editing_date = datetime.date.today()
        # 수정 내용 저장
        post.save()
        return JsonResponse({'message':'성공적으로 수정되었습니다.'},status=200)
    else:
        return_data = {'message' : '해당 게시글을 수정할 수 없습니다.'}
        return JsonResponse(return_data, status=455)



# 관리자가 게시글을 수정하는 함수
def admin_update_post(memberInfo, postInfo):
    # 게시글에 대한 검증 작업
    if not isValid_text_length(postInfo['text']):
        return JsonResponse({'message':'글의 내용이 너무 깁니다.\n3000자 제한'},status=453)

    if not isValid_title_length(postInfo['title']):
        return JsonResponse({'message':'제목이 너무 깁니다.\n30자 제한'},status=452)

    # 태그 문자열로 변환
    tag = ""
    for x in postInfo['tag']:
        tag += (x + settings.TAG_SEPERATOR)

    # 회원 객체 불러오기 - 작성자 등록
    member = Member.objects.get(id=memberInfo['id'])

    # 긍/부정, 격렬/차분, 비속어 확률과 글의 온도 획득
    params = {'text': postInfo['title'] + "\n" + postInfo['text']}

    res = requests.get(settings.BERT_SERVER, params=params).json()
    prob_p_dp = res['result']['prob_p_dp']
    prob_a_da = res['result']['prob_a_da']
    prob_slang = res['result']['prob_slang']
    temperature = res['result']['temperature']

    # 수정할 post 읽어와 수정하기
    post = Post.objects.get(post_id = post_id)
    post.title = postInfo['title']
    post.text = postInfo['text']
    post.tag = tag
    post.writer = member
    post.prob_p_dp = prob_p_dp
    post.prob_a_da = prob_a_da
    post.prob_is_slang = prob_slang
    post.temperature = temperature
    # 수정 내용 저장
    post.save()
    return JsonResponse({'message':'성공적으로 수정되었습니다.'},status=200)



# ==================================================================================================================================
#                                               게시글 삭제 관련 함수
# ==================================================================================================================================

# 사용자가 게시글을 삭제하는 함수
def user_delete_post(memberInfo,postInfo):
    member_id = memberInfo['id']
    post_id = postInfo['id']
    
    if isValid_access_post(member_id,post_id):
        try:
            post = Post.objects.get(pk = post_id)
            post.is_deleted = True
            post.save()
        except:
            return_data = {'message' : '해당 게시글이 존재하지 않습니다.'}
            return JsonResponse(return_data, status=454)

        return JsonResponse({'message' : '성공적으로 삭제되었습니다.'}, status=200)
        
    else:
        return_data = {'message' : '해당 게시글을 삭제할 수 없습니다.'}
        return JsonResponse(return_data, status=456)


# 관리자가 게시글을 삭제하는 함수
def admin_delete_post(posts):
    for post in posts:
        try:
            post = Post.objects.get(pk = post['id'])
            post.is_deleted = True
            post.save()
        except:
            return_data = {'message' : '게시글 삭제중 오류가 발생했습니다.'}
            return JsonResponse(return_data, status=456)
    return JsonResponse({'message' : '성공적으로 삭제되었습니다.'}, status=200)
    


# ==================================================================================================================================
#                                               게시글 블라인드 함수
# ==================================================================================================================================
@csrf_exempt 
def admin_blind_post(request):
    posts = json.loads(request.body.decode('utf-8'))
    print(posts)
    posts = posts['post']
    posts = posts['rows']
    for post in posts:
        try:
            post = Post.objects.get(pk = post['id'])
            post.is_blinded = True
            post.save()
        except:
            return_data = {'message' : '게시글 블라인드중 오류가 발생했습니다.'}
            return JsonResponse(return_data, status=457)
    return JsonResponse({'message' : '성공적으로 블라인드 처리되었습니다.'}, status=200)


# ==================================================================================================================================
#                                               게시글 좋아요 함수
# ==================================================================================================================================

@csrf_exempt
def user_like_post(requestm,pk):
    try:
        member_info = get_member_info(request.COOKIES)
        member = Member.objects.get(id = member_info['id'])
        post = Post.objects.get(post_id=pk)
        if LikeRecord.objects.filter(member_id = member, post_id=post).exists():
            like_record = LikeRecord.objects.get(member_id = member, post_id=post)
            like_record.delete()
            lookup_record = LookupRecord.objects.get(member_id=member,post_id=post)
            lookup_record.is_like = False
            lookup_record.save()
            post.num_good = post.num_good - 1 
            post.save()
            return JsonResponse({'message':'좋아요가 취소되었습니다.'},status=200)
        else:
            like_record = LikeRecord(member_id=member,post_id=post,temperature=post.temperature)
            like_record.save()
            lookup_record = LookupRecord.objects.get(member_id=member,post_id=post)
            lookup_record.is_like = True
            lookup_record.save()
            post.num_good = post.num_good + 1 
            post.save()

            # 알림 등록
            process_create_notice(1,post,"",member,post.writer)   # 1 : 좋아요
            
            return JsonResponse({'message':'게시글 좋아요가 등록되었습니다.'},status=200)
    except:
        return JsonResponse({'message':'게시글 좋아요 처리에 실패했습니다.'},status=458)
    


# ==================================================================================================================================
#                                               사용자 게시글 좋아요, 조회 기록 조회, 작성 게시글 조회 함수
# ==================================================================================================================================
 
@csrf_exempt
def user_read_like_post(request):
    member_info = get_member_info(request.COOKIES)
    member = Member.objects.get(id = member_info['id'])
    like_records = LikeRecord.objects.filter(member_id = member)
    datas ={}
    index = len(like_records) -1
    for record in like_records:
        datas[index] = record.get_dic()
        index -= 1
    return JsonResponse(datas)


@csrf_exempt
def user_read_lookup_post(request):
    member_info = get_member_info(request.COOKIES)
    member = Member.objects.get(id = member_info['id'])
    lookup_records = LookupRecord.objects.filter(member_id=member)
    datas = {}
    index = len(lookup_records) - 1
    for record in lookup_records:
        datas[index] = record.get_dic()
        index -= 1
    return JsonResponse(datas)

@csrf_exempt
def user_read_writed_post(request):
    member_info = get_member_info(request.COOKIES)
    member = Member.objects.get(id = member_info['id'])
    posts = Post.objects.filter(writer = member)
    datas = {}
    index = len(posts) - 1
    for post in posts:
        datas[index] = post.get_dic(False)
        index -= 1
    return JsonResponse(datas)

# ==================================================================================================================================
#                                               게시글 검증 관련 함수
# ==================================================================================================================================


# 게시글 제목 길이 검증 - 30자 이내
def isValid_title_length(title):
    maxTitleLength = 30
    if len(title) > maxTitleLength:
        return False
    else:
        return True

# 게시글 본문 길이 검증 - 3000자 이내
def isValid_text_length(text):
    maxTextLength = 3000
    if len(text) > maxTextLength:
        return False
    else:
        return True

# 게시글 권한 검증 - 게시글에 대한 수정 및 삭제 권한 확인
def isValid_access_post(member_id, post_id):
    member = Member.objects.get(id = member_id)
    post = Post.objects.filter(post_id = post_id, writer = member)

    if post is None:
        return False
    else:
        return True