from django.shortcuts import render
from django.http import JsonResponse
import datetime
from .models import Keyword
from django.views.decorators.csrf import csrf_exempt
import json
from member.jwt_manager import get_member_info
from member.models import Member
from django.conf import settings
# Create your views here.
@csrf_exempt 
def process_admin_keyword(request):
    if request.method == "GET":
        return process_admin_read(request)
    elif request.method == "POST":
        return process_admin_create(request)
    elif request.method == 'DELETE':
        return admin_keyword_delete(request)

def get_keywords_by_keyword_match(request, query):
    keywords = Keyword.objects.filter(keyword__icontains = query)
    return keywords
def get_keywords_by_registrator(request, query):
    keywords = Keyword.objects.filter(registrator = query)
    return keywords
def get_keywords_by_registration_date_upper(request, query):
    keywords = Keyword.objects.filter(registrator__lte = query)
    return keywords
def get_keywords_by_registration_date_lower(request, query):
    keywords = Keyword.objects.filter(registrator__gte = query)
    return keywords    
def get_keywords_by_recent_used_date_upper(request, query):
    keywords = Keyword.objects.filter(recent_used_date__gte = query)
    return keywords    
def get_keywords_by_recent_used_date_lower(request, query):
    keywords = Keyword.objects.filter(recent_used_date__lte = query)
    return keywords        
def get_keywords_by_suggest_amount_upper(request, query):      
    keywords = Keyword.objects.filter(suggest_amount__gte = query)
    return keywords                          
def get_keywords_by_suggest_amount_lower(request, query):                
    keywords = Keyword.objects.filter(suggest_amount__lte = query)
    return keywords        

def process_admin_read(request):
    condition_dic = {
    "키워드" : get_keywords_by_keyword_match,
    "등록자" : get_keywords_by_registrator,
    "최초 등록일(이상)" : get_keywords_by_registration_date_upper,
    "최초 등록일(이하)" : get_keywords_by_registration_date_lower,
    "최근 사용(예정)일 (이상)" : get_keywords_by_recent_used_date_upper,
    "최근 사용(예정)일 (이하)" : get_keywords_by_recent_used_date_lower,
    "사용 수(이상)" : get_keywords_by_suggest_amount_upper,
    "사용 수(이하)" : get_keywords_by_suggest_amount_lower,
    }
    function = condition_dic[request.GET.get('condition')]
    query = request.GET.get('query')
    keywords = function(request, query)
    data = {}
    idx = 0
    for keyword in keywords:
        data[idx] = keyword.get_for_admin()
        idx+=1
    return JsonResponse({'data' : data},status = 200)





def process_admin_create(request):
    keyword_info = json.loads(request.body.decode('utf-8'))
    keyword_text = keyword_info['keyword']
    try:
        to_use_date = datetime.datetime.strptime(keyword_info['to_use_date'],"%Y-%m-%d").date()
    except :
        return JsonResponse({'message':'날짜가 입력되지 않았습니다.'},status=453)
    
    # 날짜 겹치는지 체크
    if Keyword.objects.filter(suggest_date = to_use_date).count() != 0:
        return JsonResponse({'message' : '기존 키워드와 사용 예정일이 중복되었습니다.'}, status=457)

    try: # 이미 존재 하는 키워드 
        keyword = Keyword.objects.get(keyword = keyword_text)
          
        # 등록된 키워드와 최근 사용일이 30일 이상
        day_diff = abs((keyword.recent_used_date - to_use_date).days)
        if day_diff <= settings.KEYWORD_ALLOW_GAP:
            return JsonResponse({'message' : '30일 이내에 사용되었습니다.'}, status=452)
        
        day_diff = abs((keyword.suggest_date - to_use_date).days)
        if day_diff <= settings.KEYWORD_ALLOW_GAP:
            return JsonResponse({'message' : '30일 이내에 사용될 예정입니다.'}, status=452)

        keyword.suggest_date = to_use_date
        keyword.save()
        return JsonResponse({'message' : '기존 키워드의 사용 예정일이 수정되었습니다.'}, status=200)    
    except : 
        try: # 새로운 키워드일 경우
            registrator_info = get_member_info(request.COOKIES)
            registrator = Member.objects.get(id=registrator_info['id'])
            keyword = Keyword(keyword=keyword_text, suggest_date = to_use_date, registrator=registrator)
            keyword.save()
            return JsonResponse({'message' : '새로운 키워드가 등록되었습니다.'}, status=200)
        except : 
            return JsonResponse({'message' : '키워드 등록에 실패하였습니다.'}, status=453)


def admin_keyword_delete(request):
    try:
        keywords = json.loads(request.body.decode('utf-8'))
        keywords = keywords['keyword']
        keywords = keywords['rows']

        delete_count = len(keywords)
        failCount = 0

        for keyword in keywords:
            key = Keyword.objects.get(keyword = keyword['id'])
            if key.suggest_amount == 0:
                key.delete()
            else:
                failCount += 1
        if failCount == 0: 
            return JsonResponse({'message':'키워드를 정상적으로 삭제하였습니다.'},status = 200)
        elif delete_count != failCount:
            return JsonResponse({'message':'삭제 가능한 키워드만 삭제하였습니다.'},status = 454)
        else:
            return JsonResponse({'message':'키워드 삭제가 불가능합니다.'},status = 455)
    except :
        return JsonResponse({'message':'키워드 삭제중 오류가 발생하였습니다.'},status = 456)
    



def user_process_keyword(request):
    if request.method == 'GET':
        try:
            today = datetime.date.today()
            today_keyword = Keyword.objects.get(suggest_date = today)

            # 최근 사용일이 오늘이 아닌경우
            if today_keyword.recent_used_date != today:
                today_keyword.recent_used_date = today
                today_keyword.save()
            return JsonResponse({'keyword':today_keyword.get_keyword()},status = 200)
        except:
            return JsonResponse({'message':'오늘의 키워드가 존재하지 않습니다.'},status = 458)
    return JsonResponse({'message':'잘못된 요청 메소드'},status = 490)
    


    
