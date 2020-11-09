from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from .models import Member
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
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
            return_data = {'message' : '로그인 성공'}
            res = JsonResponse(return_data)
            res.set_cookie('jwt', jwt_data)
            return res
        except Exception as e:
            return_data = {'memberInfo' : None, 'message' : '로그인 실패'}
            return JsonResponse(return_data, status=410)
@csrf_exempt 
def admin_login(request):
    loginInfo = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        data = {}
        try:
            member = Member.objects.get(id=loginInfo['id'],pw=loginInfo['pw'])
            if member.authority == settings.AUTHORITY['관리자']:
                data['id'] = loginInfo['id']
                data['pw'] = loginInfo['pw']
                data['authority'] = str(member.authority)
                print(data)
                jwt_data = encode_jason_to_jwt(data)
                return_data = {'message' : '로그인 성공'}
                res = JsonResponse(return_data)
                res.set_cookie('jwt', jwt_data)
                return res
            else :
                raise Exception
        except Exception as e:
            return_data = {'memberInfo' : None, 'message' : '로그인 실패'}
            return JsonResponse(return_data, status=410)

@csrf_exempt
def register_user(request):
    registInfo = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        data ={}
        if(isValidRegistInfo(registInfo)):
            if isExistId(registInfo['id']):
                try:
                    member = Member(id=registInfo['id'],pw=registInfo['pw'],name=registInfo['name'],nickname=registInfo['nickname'],age=registInfo['age'],gender=registInfo['gender'],authority=settings.AUTHORITY['회원'],phonenumber=registInfo['phonenumber'],email=registInfo['email'])
                    member.save()
                    data['id'] = member.id
                    data['authority'] = settings.AUTHORITY['회원']
                    # print(settings.AUTHORITY['회원'])
                    jwt_data = encode_jason_to_jwt(data)
                    return_data = {'jwt':jwt_data, 'message' : '회원가입 성공'}
                    return JsonResponse(return_data)
                except Exception as e:
                    print(e)
                    return_data = {'message' : '회원가입 실패, 관리자에게 문의바랍니다.'}
                    return JsonResponse(return_data, status=410)
            else:
                return_data = {'message' : '이미 존재하는 아이디입니다.'}
                return JsonResponse(return_data, status=411)
        else:
            return_data = {'message' : '이메일 또는 전화번호를 확인하세요.'}
            return JsonResponse(return_data, status=412)

def isExistId(id):
    try :
        member = Member.objects.get(id=id)
        return False
    except:
        return True


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