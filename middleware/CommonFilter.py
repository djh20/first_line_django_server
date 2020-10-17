from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden 

class BeforeFilter(MiddlewareMixin):
    def process_request(self, request):
        print("das")



class AfterFilter(MiddlewareMixin):
    def process_response(self,request,response):
        return response 