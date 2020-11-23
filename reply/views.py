from django.shortcuts import render
from .models import Reply
import json
from django.http import JsonResponse
from member.jwt_manager import get_member_info
from django.views.decorators.csrf import csrf_exempt
from post.models import Post
from member.models import Member
from notice.views import process_create_notice
import requests, json
from django.conf import settings
from urllib import parse


# 사용자의 댓글 관련 요청 처리 함수
@csrf_exempt 
def user_process_reply(request):
    if request.method == 'GET':
        # Read 작업 - 댓글 조회(사용자) - 특정 게시글의 댓글을 조회한다
        if request.GET.get('post_id') != None:
            memberInfo = get_member_info(request.COOKIES)
            post_id = request.GET.get('post_id')
            return user_read_reply(memberInfo, post_id)

        elif request.GET.get('code') != None:
            return user_search_reply(request)

        else:
            return JsonResponse({'message' : '필수정보 누락'}, status = 489)

    elif request.method == 'POST':
        # Create 작업 - 댓글 등록(사용자)
        member_info = get_member_info(request.COOKIES)
        reply_info = json.loads(request.body.decode('utf-8'))
        return create_reply(member_info, reply_info)

    elif request.method == 'PUT':
        # Update 작업 - 댓글 수정(사용자)
        member_info = get_member_info(request.COOKIES)
        reply_info = json.loads(request.body.decode('utf-8'))
        return user_update_reply(member_info, reply_info)

    else :
        # Delete 작업 - 댓글 삭제(사용자) 
        member_info = get_member_info(request.COOKIES)
        reply_info = json.loads(request.body.decode('utf-8'))
        return user_delete_reply(member_info, reply_info)
 
# 관리자의 댓글 관련 요청 처리 함수
@csrf_exempt 
def admin_process_reply(request):
    if request.method == 'GET':
        # Read 작업 - 댓글 조회(관리자)
        if request.GET.get('code') != None:
            return admin_search_reply(request)
        else:
            return admin_read_all_reply()

    elif request.method == 'POST':
        # Create 작업 - 댓글 등록(관리자)
        member_info = get_member_info(request.COOKIES)
        reply_info = json.loads(request.body.decode('utf-8'))
        return create_reply(member_info, reply_info)
    elif request.method == 'PUT':
        # Update 작업 - 댓글 수정(관리자)
        member_info = get_member_info(request.COOKIES)
        reply_info = json.loads(request.body.decode('utf-8'))
        return admin_update_reply(member_info, reply_info)

    else :
        # Delete 작업 - 댓글 삭제(관리자)
        replies = json.loads(request.body.decode('utf-8'))
        replies = replies['reply']
        replies = replies['rows']
        return admin_delete_reply(replies)



# ==============================================================================================
#                                       댓글 검색 함수 모음
# ==============================================================================================

def user_search_reply(request):
    memberInfo = get_member_info(request.COOKIES)
    code = int(request.GET.get('code'))
    query = parse.unquote(request.GET.get('query'))
    return search_reply(code,query,False,memberInfo)

def admin_search_reply(request):
    try:
        search_code = int(request.GET.get('code'))
        query = parse.unquote(request.GET.get('query'))

        return search_reply(search_code,query,True)         
    except Exception as e :
        print(e)
        return JsonResponse({'message':'댓글 검색중 오류가 발생했습니다.'}, status=458)

def search_reply(search_code,query,isAdmin,memberInfo = None):
    if query == '':
        datas = search_reply_entire(isAdmin,memberInfo)
        return JsonResponse(datas, status = 200)
    code ={'댓글 번호 (이상)':0,'댓글 번호 (이하)':1,"게시글 번호 (이상)":2,"게시글 번호 (이하)":3, '내용':4,'작성자':5,'작성일 (이후)':6,
        '작성일 (이전)':7, '수정일(이후)':8,'수정일(이전)':9,'욕설 확률 (이상)':10,'욕설 확률 (이하)':11,'삭제 여부':12,'블라인드 여부':13 ,'전체':14}
    

    if code['댓글 번호 (이상)']==search_code:
        datas = search_reply_num_over(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['댓글 번호 (이하)'] == search_code:
        datas = search_reply_num_under(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['게시글 번호 (이상)'] == search_code:
        datas = search_reply_post_num_over(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['게시글 번호 (이하)'] == search_code:
        datas = search_reply_post_num_under(query,isAdmin)
        return JsonResponse(datas, status = 200)
    
    elif code['내용'] == search_code:
        datas = search_reply_text(query,isAdmin,memberInfo)
        return JsonResponse(datas, status = 200)

    elif code['작성자'] == search_code:
        datas = search_reply_writer(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['작성일 (이후)'] == search_code:
        datas = search_reply_writing_date_after(query,isAdmin,memberInfo)
        return JsonResponse(datas, status = 200)

    elif code['작성일 (이전)'] == search_code:
        datas = search_reply_writing_date_before(query,isAdmin,memberInfo)
        return JsonResponse(datas, status = 200)

    elif code['수정일(이후)'] == search_code:
        datas = search_reply_edting_date_after(query,isAdmin,memberInfo)
        return JsonResponse(datas, status = 200)

    elif code['수정일(이전)'] == search_code:
        datas = search_reply_edting_date_before(query,isAdmin,memberInfo)
        return JsonResponse(datas, status = 200)

    elif code['욕설 확률 (이상)'] == search_code:
        datas = search_reply_slang_over(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['욕설 확률 (이하)'] == search_code:
        datas = search_reply_slang_under(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['삭제 여부'] == search_code:
        datas = search_reply_is_deleted(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['블라인드 여부'] == search_code:
        datas = search_reply_is_blinded(query,isAdmin)
        return JsonResponse(datas, status = 200)

    elif code['전체'] == search_code:
        datas = search_reply_entire_query(query,isAdmin)
        return JsonResponse(datas, status = 200)


def search_reply_entire(isAdmin, memberInfo = None):
    datas ={}
    if isAdmin:
        replies = Reply.objects.all()
    else:
        member = Member.objects.get(id=memberInfo['id'])
        replies = Reply.objects.filter(writer=member, is_deleted= False)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas
    

def search_reply_num_over(query,isAdmin):
    datas ={}
    replies = Reply.objects.filter(reply_id__gte = query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_num_under(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(reply_id__lte = query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_post_num_over(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(post_id_id__gte = query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_post_num_under(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(post_id_id__lte = query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_text(query, isAdmin, memberInfo = None):
    datas ={}
    if isAdmin:
        replies = Reply.objects.filter(text__contains = query)
    else:
        member = Member.objects.get(id = memberInfo['id'])
        replies = Reply.objects.filter(text__contains = query, writer = member, is_deleted = False)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_writer(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(writer__nickname__contains = query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_writing_date_after(query, isAdmin, memberInfo = None):
    datas ={}
    if isAdmin:
        replies = Reply.objects.filter(writing_date__gte = query)
    else:
        member = Member.objects.get(id = memberInfo['id'])
        replies = Reply.objects.filter(writing_date__gte = query, writer = member, is_deleted = False)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_writing_date_before(query, isAdmin, memberInfo = None):
    datas ={}
    if isAdmin:
        replies = Reply.objects.filter(writing_date__lte = query)
    else:
        member = Member.objects.get(id = memberInfo['id'])
        replies = Reply.objects.filter(writing_date__lte = query, writer = member, is_deleted = False)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_edting_date_after(query, isAdmin, memberInfo = None):
    datas ={}
    if isAdmin:
        replies = Reply.objects.filter(editing_date__gte = query).exclude(editing_date = None)
    else:
        member = Member.objects.get(id = memberInfo['id'])
        replies = Reply.objects.filter(editing_date__gte = query, writer = member, is_deleted = False).exclude(editing_date = None)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_edting_date_before(query, isAdmin, memberInfo = None):
    datas ={}
    if isAdmin:
        replies = Reply.objects.filter(editing_date__lte = query).exclude(editing_date = None)
    else:
        member = Member.objects.get(id = memberInfo['id'])
        replies = Reply.objects.filter(editing_date__lte = query, writer = member, is_deleted = False).exclude(editing_date = None)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_slang_over(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(prob_is_slang__gte =  query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_slang_under(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(prob_is_slang__lte =  query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_is_deleted(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(is_deleted =  query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_is_blinded(query, isAdmin):
    datas ={}
    replies = Reply.objects.filter(is_blinded =  query)
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas

def search_reply_entire_query(query, isAdmin):
    datas ={}
    r1 = Reply.objects.filter(writer__nickname__contains = query)
    r2 = Reply.objects.filter(text__contains = query)
    replies = r1 | r2
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(isAdmin)
        index -= 1
    return datas



# =========================================================================
#                             댓글 등록
# =========================================================================

def create_reply(memberInfo,replyInfo):
    if memberInfo != None:
        try:
            # 길이 검증
            if not isValid_reply_length(replyInfo['text']):
                return JsonResponse({'message':'댓글이 너무 깁니다.'},status=452)

            member = Member.objects.get(id = memberInfo['id'])
            post = Post.objects.get(post_id=int(replyInfo['post_id']))

            params = {'text': replyInfo['text']}
            res = requests.get(settings.BERT_SERVER, params = params).json()
    
            prob_slang = res['result']['prob_slang']
 
            prob_slang = 0
            reply = Reply(post_id = post, writer = member,text = replyInfo['text'], prob_is_slang=prob_slang)
            reply.save()
            post.num_reply = post.num_reply + 1
            post.save()

            # 게시글 작성자에게 알림 전송 - 게시글 작성자가 아닌 사람이 댓글을 작성한 경우
            if post.writer.id != member.id:
                process_create_notice(0,post.post_id,replyInfo['text'],member,post.writer) # 0:댓글

            return JsonResponse({'message':"댓글 등록 성공"}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message':"댓글 등록 실패"}, status=453)
    else:
        return JsonResponse({'message':"댓글 등록 실패"}, status=453)



# =========================================================================
#                             댓글 조회
# =========================================================================

def user_read_reply(memberInfo, postId):
    try:
        member = Member.objects.get(id = memberInfo['id'])
        member_id = member.id

        # 삭제되지 않은 댓글들을 조회
        replies = Reply.objects.filter(post_id=postId).exclude(is_deleted = True)
        datas = {}
        isMine = {}
        reply_num = 0
        for reply in replies:
            datas[reply_num] = reply.get_dic(False)
            # 조회자 == 댓글 작성자를 확인
            if member_id == reply.writer.id:
                isMine[reply_num] = True
            else:
                isMine[reply_num] = False
            reply_num += 1         
        return JsonResponse({'datas':datas,'isMine':isMine},status = 200)
    except Exception as e:
        print(e)
        return JsonResponse({'message':"댓글이 존재하지 않습니다"}, status=454)


def user_read_writed_reply(request):
    member_info = get_member_info(request.COOKIES)
    member = Member.objects.get(id = member_info['id'])
    replies = Reply.objects.filter(writer = member)
    datas = {}
    index = len(replies) - 1
    for reply in replies:
        datas[index] = reply.get_dic(False)
        index -= 1
    return JsonResponse(datas, status = 200)


def admin_read_all_reply():
    datas = {}
    replies = Reply.objects.all()
    reply_num = len(replies)-1
    for reply in replies:
        datas[reply_num] = reply.get_dic(True)
        reply_num -= 1
    return JsonResponse(datas, status = 200)


# =========================================================================
#                             댓글 수정
# =========================================================================


def user_update_reply(memberInfo, replyInfo):
    if isValid_access_reply(memberInfo['id'],replyInfo['id']):
        reply = Reply.objects.get(pk = replyInfo['id'])
        reply.text = replyInfo['text']
        
        # 댓글에 대한 비속어 확률 예측
        params = {'text': replyInfo['text']}
        res = requests.get(settings.BERT_SERVER, params = params).json()
        prob_slang = res['result']['prob_slang']

        reply.prob_is_slang = prob_slang
        reply.save()

        return JsonResponse({'message':'댓글이 수정되었습니다.'},status=200)
    else:
        return JsonResponse({'message':'댓글 수정에 실패하였습니다.'},status=455)
    



def admin_update_reply(memberInfo, replyInfo):
    member = Member.objects.get(id=memberInfo['id'])
    reply = Reply.objects.get(pk = replyInfo['id'])
    reply.text = replyInfo['text']
    reply.writer = member

    # 댓글에 대한 비속어 확률 예측
    params = {'text': replyInfo['text']}
    res = requests.get(settings.BERT_SERVER, params = params).json()
    prob_slang = res['result']['prob_slang']

    reply.prob_is_slang = prob_slang
    reply.save()

    return JsonResponse({'message':'댓글이 수정되었습니다.'},status=200)






# =========================================================================
#                             댓글 삭제
# =========================================================================


def user_delete_reply(memberInfo, replyInfo):
    if isValid_access_reply(memberInfo['id'],replyInfo['id']):
        reply = Reply.objects.get(pk= replyInfo['id'])
        reply.is_deleted = True
        reply.post_id.num_reply = reply.post_id.num_reply - 1
        reply.post_id.save()
        reply.save()
        return JsonResponse({'message': '댓글이 삭제되었습니다.'},status=200)
    else:

        return JsonResponse({'message':'댓글 삭제를 실패하였습니다.'},status=455)



def admin_delete_reply(replies):
    try:
        for reply_info in replies:
            reply = Reply.objects.get(pk = reply_info['id'])
            reply.is_deleted = True
            reply.post_id.num_reply = reply.post_id.num_reply - 1
            reply.post_id.save()
            reply.save()
        return JsonResponse({'message': '댓글이 삭제되었습니다.'},status=200)
    except:
        return JsonResponse({'message':'댓글 삭제중 오류가 발생했습니다.'},status=456)
    

# =========================================================================
#                             댓글 블라인드
# =========================================================================

@csrf_exempt
def admin_blind_reply(request):
    try:
        replies = json.loads(request.body.decode('utf-8'))
        replies = replies['reply']
        replies = replies['rows']
        for reply_info in replies:
            reply = Reply.objects.get(pk = reply_info['id'])
            reply.is_blinded = True
            reply.save()
        return JsonResponse({'message': '댓글이 블라인드 처리되었습니다.'},status=200)
    except:
        return JsonResponse({'message':'댓글 블라인드 처리중 오류가 발생했습니다.'},status=457)



# =========================================================================
#                             댓글 검증
# =========================================================================

# 댓글 길이 검증
def isValid_reply_length(text):
    maxTextLength = 3000
    if len(text) > maxTextLength:
        return False
    else:
        return True

def isValid_access_reply(member_id,reply_id):
    member = Member.objects.get(id = member_id)
    if Reply.objects.filter(pk = reply_id, writer = member).exists():
        return True
    else:
        return False