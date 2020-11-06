from django.shortcuts import render
from .models import Notice
from django.http import JsonResponse
# Create your views here.
rowsPerPage = 20

def admin_search_notice(request):
    if request.method == "GET":
        condition_dic = {
             "알림번호" : "notice_id", 
             "수신ID": "receiver_id", 
             "발신ID": "sender_id",
             "내용" : "send_datetime", 
             "발신 시각" : "text", 
             "읽음" : "is_read"
        }
        print(request.GET.get('condition'))
        condition = condition_dic[request.GET.get('condition')]
        
        query = request.GET.get('query')
        
        notices, currentPage, totalPage = get_text_match(query,1)
        data = {}
        idx = 0
        for notice in notices:
            data[idx] = notice.get_for_admin()
            idx+=1
        return JsonResponse({'data' : data, 'currentPage' : currentPage, 'totalPage' : totalPage})
    return JsonResponse({'message' : "존재하지 않는 요청"})

def get_text_match(query, currentPage):
    notices = Notice.objects.filter(text__icontains = query)
    totalPage = int(len(notices)/rowsPerPage)+1
    return notices, currentPage, totalPage