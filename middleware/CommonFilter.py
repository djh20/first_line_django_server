from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden 
from django.conf import settings
from member.jwt_manager import get_authoritiy_info

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
        return response 