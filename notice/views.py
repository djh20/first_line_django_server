from django.shortcuts import render
from .models import Notice
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from member.models import Member
from member.jwt_manager import get_member_info
# Create your views here.
rowsPerPage = 20

@csrf_exempt 
def process_admin_notice(request):
    if request.method == "GET":
        return process_admin_read(request)
    if request.method == "POST":
        return process_admin_create(request)
    return JsonResponse({'message' : "잘못된 요청 메소드"},status=490)

def process_admin_create(request):
    notice_info = json.loads(request.body.decode('utf-8'))
    try:
        receiver = Member.objects.get(id=notice_info['receiver_id'])
        try : 
            sender = Member.objects.get(id=notice_info['sender_id'])
            try : 
                text = notice_info['text']
                source_url = notice_info['source_url']
                if(len(text) < 1): 
                    raise Exception("error")
                notice = Notice(receiver_id=receiver, sender_id=sender, text = text , source_url=source_url)
                notice.save()
                return JsonResponse({'message' : "등록에 성공했습니다"}, status=200)
            except Exception as e:
                return JsonResponse({'message' : "내용 누락"}, status=452)    
        except Exception as e:
            return JsonResponse({'message' : "존재 하지 않는 발신자"}, status=453)
    except Exception as e:
        return JsonResponse({'message' : "존재 하지 않는 수신자"}, status=454)



def get_notices_by_notice_id(request, query):
    notices = Notice.objects.filter(notice_id = query)
    return notices

def get_notices_by_receiver_id(request, query):
    notices = Notice.objects.filter(receiver_id = query)
    return notices

def get_notices_by_sender_id(request, query):
    notices = Notice.objects.filter(sender_id = query)
    return notices

def get_notices_by_send_datetime_upper(request, query):
    notices = Notice.objects.filter(send_datetime__gte = query)
    return notices

def get_notices_by_send_datetime_lower(request, query):
    notices = Notice.objects.filter(send_datetime__lte = query)
    return notices

def get_notices_by_is_read(request, query):
    notices = Notice.objects.filter(is_read = query)
    return notices

def get_notices_by_contaion_text(request, query):
    notices = Notice.objects.filter(text__icontains = query)
    return notices

def get_notices_by_all(reuest, query):
    n1 = Notice.objects.filter(text__icontains = query)
    n2 = Notice.objects.filter(sender_id__id__contains = query)
    n3 = Notice.objects.filter(receiver_id__id__contains = query)
    notices = n1 | n2 | n3
    return notices

def process_admin_read(request):
    condition_dic = {
        "알림 번호" : get_notices_by_notice_id, 
        "수신 ID": get_notices_by_receiver_id, 
        "발신 ID": get_notices_by_sender_id,
        "내용" : get_notices_by_contaion_text, 
        "발신 시각(이상)" : get_notices_by_send_datetime_upper, 
        "발신 시각(이하)" : get_notices_by_send_datetime_lower, 
        "읽음" : get_notices_by_is_read,
        "전체" : get_notices_by_all,
    }
    function = condition_dic[request.GET.get('condition')]
    query = request.GET.get('query')
    notices = function(request, query)
    data = {}
    idx = 0
    for notice in notices:
        data[idx] = notice.get_for_admin()
        idx+=1
    return JsonResponse({'data' : data},status=200)

def get_text_match(query, currentPage):
    notices = Notice.objects.filter(text__icontains = query)
    totalPage = int(len(notices)/rowsPerPage)+1
    return notices, currentPage, totalPage

@csrf_exempt 
def process_user_notice(request):
    try:
        if request.method == "GET":
            return process_read_my_notice(request)
        if request.method == "DELETE":
            return process_delete_my_notice(request)
    except :
        return JsonResponse({'message' : '잘못된 요청 메소드'}, status=490)

def process_read_my_notice(request):
    try:
        data = {}
        member_info = get_member_info(request.COOKIES)
        member = Member.objects.get(id=member_info['id'])
        notices = Notice.objects.filter(receiver_id=member, is_read=False)
        idx = len(notices)-1
        for notice in notices:
            if notice.is_read == False:
                data[idx] = notice.get_for_user()
                idx-=1
        return JsonResponse({'data' : data}, status=200)
    except:
        return JsonResponse({'message' : '알림 조회 실패'}, status=455)
            
@csrf_exempt 
def process_delete_my_notice(request):
    try:
        notice_id = json.loads(request.body.decode('utf-8'))['notice_id']
        notice = Notice.objects.get(notice_id= notice_id)
        notice.is_read = True
        notice.save()
        return JsonResponse({'message' : '삭제 성공'}, status=200)
    except :
        return JsonResponse({'message' : '알림 삭제 실패'}, status=456)



def process_create_notice(notice_code,post_id,text,sender,receiver):
    code = {'댓글':0,'좋아요':1}
    try:
        url = '/post/detail/'+str(post_id)
        if code['댓글'] == int(notice_code):
            store_text = "{}님이 내 게시글에 댓글을 남겼습니다. : {} ".format(sender.nickname,text)
        elif code['좋아요'] == int(notice_code):
            store_text = "{}님이 내 게시글에 좋아요를 남겼습니다".format(sender.nickname)
        new_notice = Notice(receiver_id=receiver,sender_id=sender,text=store_text,source_url=url)
        new_notice.save()
    except:
        print("알림등록에 실패하였습니다.")
        print("post_id : {}\n sender : {}\nreceiver : {}\ntext : {}".format(post_id,sender,receiver,text))
    

