from django.shortcuts import render
from .models import Log, LoginLog
from member.models import Member


# Create your views here.
def admin_process_log(request):
    if request.method == 'GET':
        # 로그 내역 조회
        pass



# requester는 요청자 정보
def create_request_log(request_ip,request_method,url,requester=None):
    if requester_id != None:
        member = Member.objects.get(id = requester['id'])
        request_log = Log(requester_ip = request_ip, request_method=request_method, url=url, requester_id = member)
    else:
        request_log = Log(requester_ip = request_ip, request_method=request_method, url=url)
    request_log.save()

def create_response_log(request_ip,request_method,url,result_code,result_code_detail):
    pass



def read_log():
    pass

def admin_read_login_log():
    datas = {}
    logs = LoginLog.objects.all()
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas)

def user_read_login_log(request):
    
    datas = {}
    member = Member.objects.get(id = memberInfo['id'])
    logs = LoginLog.objects.filter(login_id = member.id)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas)


