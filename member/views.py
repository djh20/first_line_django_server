from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from .models import Member
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .jwt_manager import *
@csrf_exempt 
def login(request):
    loginInfo = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        data = {}
        try:
            member = MemberInfo.objects.get(id=loginInfo['id'],pw=loginInfo['pw'])
            data['id'] = loginInfo['id']
            data['pw'] = loginInfo['pw']
            jwt_data = encode_jason_to_jwt(data)
            return_data = {'jwt' : jwt_data, 'message' : '로그인 성공'}
            return JsonResponse(return_data)
        except Exception as e:
            return_data = {'memberInfo' : None, 'message' : '로그인 실패'}
            return JsonResponse(return_data, status=410)
            