from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden 
from django.conf import settings
from member.jwt_manager import get_authoritiy_info, get_member_info
import re
from log.models import Log, ResultCode
from log.views import create_log, create_Login_log
from member.models import Member
import json

class BeforeFilter(MiddlewareMixin):
    # print("")
    # 테스트 기간 비활성화
    def process_request(self, request):
        print(request.COOKIES)
        # if self.validate_authority(request) == False:
            # return HttpResponseForbidden()
        
    
    def validate_authority(self,request):
        if request.path in settings.URLS_AUTHORITY :
            user_authority = get_authoritiy_info(request.COOKIES)
            print(user_authority)
            if settings.URLS_AUTHORITY[request.path] <= user_authority:
                return True
        return False




class AfterFilter(MiddlewareMixin):
    def process_response(self,request,response):
        #######   로그 남기기   #######
        field = self.get_code(request.path)
        print("필드 {}, 코드 {}".format(field,response.status_code))
        
        # 지정한 코드가 아닌경우 => 세계에서 약속된 코드인경우 detail은 존재하지 않음
        try:
            resultCode_detail = ResultCode.objects.get(field = field, code = response.status_code)
            code_detail = resultCode_detail.code_detail
        except:
            code_detail = ''
        
        url = request.path
        try:
            memberInfo = get_member_info(request.COOKIES)
            member = Member.objects.get(id = memberInfo['id'])
            create_log(request_ip=request.get_host(), request_method=request.method, url=url, result_code=response.status_code, result_code_detail=code_detail, requester=member)
        except Exception as e:
            create_log(request_ip=request.get_host(), request_method=request.method, url=url, result_code=response.status_code, result_code_detail=code_detail)
        ###############################

        #####  로그인 로그 남기기  #####
        isLogin = re.compile('.*member\/login\/')
        isLogin2 = re.compile('.*member\/admin\/login\/')
        if isLogin.match(url) or isLogin2.mathc(url):
            loginInfo = json.loads(request.body.decode('utf-8'))
            login_id = loginInfo['id']
            create_Login_log(requester_ip=request.get_host(),login_id=login_id,login_result=(True if response.status_code == 200 else False))
        ###############################

        return response 

    def get_code(self,url):
        isMember = re.compile('.*member\/+')
        isPost = re.compile('.*post\/+')
        isReply = re.compile('.*reply\/+')
        isNotice = re.compile('.*notice\/+')
        isReport = re.compile('.*report\/+')
        isLog = re.compile('.*log\/+')
        isKeyword = re.compile('.*keyword/+')

        if isMember.match(url):
            return 1
        elif isPost.match(url):
            return 2
        elif isReply.match(url):
            return 3
        elif isNotice.match(url):
            return 4
        elif isReport.match(url):
            return 5
        elif isLog.match(url):
            return 7
        elif isKeyword.match(url):
            return 6
