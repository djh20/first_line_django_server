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
    to_use_date = datetime.datetime.strptime(keyword_info['to_use_date'],"%Y-%m-%d").date()
    try: # 이미 존재 하는 키워드 
        keyword = Keyword.objects.filter(keyword = keyword_text).first()
        day_diff = abs((keyword.recent_used_date - to_use_date).days)
        try : # 등록된 키워드와 최근 사용일이 30일 이상
            if day_diff <= settings.KEYWORD_ALLOW_GAP:
                raise Exception
            keyword.suggest_amount += 1
            keyword.recent_used_date = to_use_date
            keyword.save()
            return JsonResponse({'message' : '기존 키워드의 사용 예정일이 수정되었습니다'}, status=200)
        except: # 30일 이하
            return JsonResponse({'message' : '30일 이내에 사용되었거나 사용될 예정입니다'}, status=452)
    except : 
        try: # 새로운 키워드일 경우
            registrator_info = get_member_info(request.COOKIES)
            registrator = Member.objects.get(id=registrator_info['id'])
            keyword = Keyword(keyword=keyword_text, recent_used_date = to_use_date, registrator=registrator)
            keyword.save()
            return JsonResponse({'message' : '새로운 키워드가 등록되었습니다'}, status=200)
        except : 
            return JsonResponse({'message' : '권한이 없습니다'}, status=453)




    
