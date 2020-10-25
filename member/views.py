from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from .models import Member
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .jwt_manager import *
import re

@csrf_exempt 
def login(request):
    loginInfo = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        data = {}
        try:
            member = Member.objects.get(id=loginInfo['id'],pw=loginInfo['pw'])
            data['id'] = loginInfo['id']
            data['pw'] = loginInfo['pw']
            data['authority'] = str(member.authority)
            print(data)
            jwt_data = encode_jason_to_jwt(data)
            return_data = {'jwt' : jwt_data, 'message' : '로그인 성공'}
            return JsonResponse(return_data)
        except Exception as e:
            return_data = {'memberInfo' : None, 'message' : '로그인 실패'}
            return JsonResponse(return_data, status=410)

@csrf_exempt
def register_user(request):
    registInfo = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        data ={}
        if(isValidRegistInfo(registInfo)):
            try:

                member = Member(id=registInfo['id'],pw=registInfo['pw'],name=registInfo['name'],nickname=registInfo['nickname'],age=registInfo['age'],gender=registInfo['gender'],authority=registInfo['authority'],phonenumber=registInfo['phonenumber'],email=registInfo['email'])
                
                member.save()
                data['id'] = registInfo['id']
                data['pw'] = registInfo['pw']
                registInfo['authority'] = registInfo['authority']
                jwt_data = encode_jason_to_jwt(data)
                return_data = {'jwt':jwt_data, 'message' : '회원가입 성공'}
                return JsonResponse(return_data)
            except Exception as e:
                return_data = {'registInfo':None, 'message' : '회원가입 실패'}
                return JsonResponse(return_data, status=410)
        else:
            return_data = {'registInfo':None, 'message' : '회원가입 실패\n이메일 또는 전화번호를 확인하세요.'}
            return JsonResponse(return_data, status=410)

def isValidRegistInfo(registInfo):
    valid = True
    phoneNumberCheck = re.compile('[0-9]{2,3}-[0-9]{3,4}-[0-9]{4,4}')
    emailCheck = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    
    email = registInfo['email']
    phoneNumber = registInfo['phonenumber']
    # 이메일 처리
    if not emailCheck.match(email):
        valid = False
    
    if not phoneNumberCheck.match(phoneNumber):
        valid = False

    return valid