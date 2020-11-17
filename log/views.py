from django.shortcuts import render
from .models import Log, LoginLog, ResultCode
from member.models import Member


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
    log_search_code = {'요청IP':1,'요청자':2,'url':3,'로그일자(이상)':4,'로그일자(이하)':5,'결과':6, '특정결과':7}

    if log_search_code['요청IP'] == code:
        pass
    elif log_search_code['요청자'] == code:
        pass
    elif log_search_code['url'] == code:
        pass
    elif log_search_code['로그일자(이상)'] == code:
        pass
    elif log_search_code['로그일자(이하)'] == code:
        pass
    elif log_search_code['결과'] == code:
        pass
    elif log_search_code['특정결과'] == code:
        pass



def read_all_log():
    datas ={}
    logs = Log.objects.all()
    index = len(logs) - 1
    for log in logs:
        datas[index] = log.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)


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



