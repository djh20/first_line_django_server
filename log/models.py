from django.db import models

# Create your models here.

class Log(models.Model):
    log_id = models.AutoField(primary_key = True)
    requester_ip = models.TextField(max_length = 40)                                # IPv6의 최대길이 32 + 구분자 7 = 39
    requester_id = .ForeignKey(Member, on_delete=models.CASCADE,default = None)     # 해당 request 를 보낸 ip 주소
    request_method = models.TextField(max_length = 10)                              # GET POST PUT DELETE
    url = models.TextField(max_length = 20)                                         # request 처리를 수행하는 url
    logging_date = models.DateTimeField(auto_now_add = True)                        # 해당 로그가 발생한 일자
    result_code = models.IntegerField()                                             # request에 대한 처리 결과 코드
    result_code_detail = models.TextField(max_length = 100)                         # request에 대한 처리 상세 내용
    isRequest = models.BooleanField(null = False)

    def get_dic(self):
        return {
            'log_id' : self.log_id,
            'requester_ip' : self.requester_ip,
            'requester_id' : self.requester_id,
            'request_method' : self.request_method,
            'url' : self.url,
            'logging_date' : self.logging_date,
            'result_code' : self.result_code,
            'result_code_detail' : self.result_code_detail,
            'isRequest' : ('요청' if self.isRequest else '응답'),
        }


class LoginLog(models.Model):
    login_log_id = models.AutoField(primary_key = True)
    requester_ip = models.TextField(max_length = 40)
    login_id = models.TextField(max_length = 40)
    logging_date = models.DateTimeField(auto_now_add = True)
    login_result = models.TextField(max_length = 2)     # 성공, 실패

    def get_dic(self):
        return {
            'login_log_id' : self.login_log_id,
            'requester_ip' : self.requester_ip,
            'login_id' : self.login_id,
            'logging_date' : self.logging_date,
            'login_result' : self.login_result,
        }
