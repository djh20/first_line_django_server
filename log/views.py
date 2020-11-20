from django.shortcuts import render
from django.http import JsonResponse
from .models import Log, LoginLog, ResultCode
from member.models import Member
from member.jwt_manager import get_member_info


# Create your views here.
def admin_process_log(request):
    if request.method == 'GET':
        # 로그 내역 조회
        code = int(request.GET.get('code'))
        query = request.GET.get('query')
        return search_log(code,query)

# requester는 요청자 정보
def create_log(request_ip, request_method, url, result_code, result_code_detail, requester=None):
       
    if requester != None:
        member = Member.objects.get(id = requester['id'])
        request_log = Log(requester_ip = request_ip, request_method=request_method, url=url,result_code = result_code, result_code_detail= result_code_detail, requester_id = member)
    else:
        request_log = Log(requester_ip = request_ip, request_method=request_method, url=url,result_code = result_code, result_code_detail= result_code_detail)
    request_log.save()

def create_Login_log(requester_ip,login_id,login_result):
    result = {True:'성공', False:'실패'}
    login_log = LoginLog(requester_ip=requester_ip,login_id=login_id,login_result=result[login_result])
    login_log.save()
    

def search_log(code,query):
    if query == '':
        return read_all_log()

    log_search_code = {'전체':0 ,'요청IP':1,'요청자':2,'url':3,'로그일자(이전)':4,'로그일자(이후)':5,'결과':6, '특정결과':7}

    if log_search_code['전체'] == code:
        return read_all_log()

    elif log_search_code['요청IP'] == code:
        datas = search_log_ip(query)
        return JsonResponse(datas,status =200)

    elif log_search_code['요청자'] == code:
        datas = search_log_requester(query)
        return JsonResponse(datas,status =200)

    elif log_search_code['url'] == code:
        datas = search_log_url(query)
        return JsonResponse(datas,status =200)

    elif log_search_code['로그일자(이전)'] == code:
        datas = search_log_day_before(query)
        return JsonResponse(datas,status =200)

    elif log_search_code['로그일자(이후)'] == code:
        datas = search_log_day_after(query)
        return JsonResponse(datas,status =200)

    elif log_search_code['결과'] == code:
        datas = search_log_result(query)
        return JsonResponse(datas,status =200)

    elif log_search_code['특정결과'] == code:
        datas = search_log_result_code(query)
        return JsonResponse(datas,status =200)



def read_all_log():
    datas ={}
    logs = Log.objects.all()
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)


def search_log_ip(query):
    datas = {}
    logs = Log.objects.filter(requester_ip__contains=query)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)

def search_log_requester(query):
    datas = {}
    member = Member.objects.get(id = query)
    logs = Log.objects.filter(requester_id = member)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)

def search_log_url(query):
    datas = {}
    logs = Log.objects.filter(url__contains=query)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)

def search_log_day_before(query):
    datas = {}
    logs = Log.objects.filter(logging_date__lte=query)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)

def search_log_day_after(query):
    datas = {}
    logs = Log.objects.filter(logging_date__gte=query)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)

def search_log_result(query):
    datas = {}
    logs = Log.objects.filter(result_code_detail__contains=query)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)

def search_log_result_code(query):
    datas = {}
    logs = Log.objects.filter(result_code = query)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)


def admin_read_login_log(request):
    datas = {}
    logs = LoginLog.objects.all()
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas,status = 200)

def user_read_login_log(request):
    datas = {}
    memberInfo = get_member_info(request.COOKIES)
    member = Member.objects.get(id = memberInfo['id'])
    logs = LoginLog.objects.filter(login_id = member.id)
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas,status = 200)



