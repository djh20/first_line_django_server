from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from .models import Member, SementicRecord
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
from .jwt_manager import *
import re
import bcrypt
import datetime
from dateutil.relativedelta import relativedelta
from urllib import parse



@csrf_exempt
def user_process_info(request):
    if request.method == 'GET':
        # 사용자 정보 조회
        member_info = get_member_info(request.COOKIES)
        return user_read_info(member_info)

    elif request.method == 'POST':
        # 회원가입
        registInfo = json.loads(request.body.decode('utf-8'))
        return user_create_info(registInfo)

    elif request.method == 'PUT':
        # 사용자 정보 수정
        newInfo = json.loads(request.body.decode('utf-8'))
        newInfo = newInfo['member']
        member_info = get_member_info(request.COOKIES)
        return user_update_info(member_info, newInfo)


    elif request.method == "DELETE":
        # 사용자 정보 삭제 - 회원 탈퇴
        member_info = get_member_info(request.COOKIES)
        return user_delete_info(member_info)



@csrf_exempt
def admin_process_info(request):
    if request.method == 'GET':
        # 사용자 정보 전체 조회
        if request.GET.get('code') != None:
            code = int(request.GET.get('code'))
            query = parse.unquote(request.GET.get('query'))
            return admin_search_member(code,query)
        else:
            return admin_read_all_info()

    elif request.method == 'POST':
        # 관리자 추가
        registInfo = json.loads(request.body.decode('utf-8'))
        return admin_create_info(registInfo)

    elif request.method == 'PUT':
        # 특정 사용자 정보 수정
        newInfo = json.loads(request.body.decode('utf-8'))
        newInfo = newInfo['member']
        return admin_update_info(newInfo)

    elif request.method == "DELETE":
        # 특정 사용자 정보 삭제 - react 에서 어떤 식으로 보내는지에 따라 parsing 이 달라짐 
        # => 최종적으로는 member 객체들이 admin_delete_info 의 인자로 넘어가야함
        member_infos = json.loads(request.body.decode('utf-8'))
        member_infos = member_infos['member']
        member_infos = member_infos['rows']
        return admin_delete_info(member_infos)



@csrf_exempt 
def login(request):
    loginInfo = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        data = {}
        try:
            member = Member.objects.get(id=loginInfo['id'])
            password = member.pw
            if not bcrypt.checkpw(loginInfo['pw'].encode('utf-8') ,password.encode('utf-8')):
                raise Exception('로그인 실패') 

            data['id'] = loginInfo['id']
            data['pw'] = loginInfo['pw']
            data['authority'] = str(member.authority)

            jwt_data = encode_jason_to_jwt(data)
            return_data = {'message' : '로그인 성공'}
            res = JsonResponse(return_data, status = 200)
            res.set_cookie('jwt', jwt_data)
            return res
        except Exception as e:
            return_data = {'memberInfo' : None, 'message' : '로그인 실패'}
            return JsonResponse(return_data, status=452)

@csrf_exempt 
def admin_login(request):
    loginInfo = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        data = {}
        try:
            member = Member.objects.get(id=loginInfo['id'])
            try :
                if member.authority != settings.AUTHORITY['관리자']:
                    raise Exception("비정상적인 접근")
            except Exception as e:
                return_data = {'memberInfo' : None, 'message' : '비정상적인 접근'}
                return JsonResponse(return_data, status=487)
            password = member.pw
            print(password)
            if not bcrypt.checkpw(loginInfo['pw'].encode('utf-8') ,password.encode('utf-8')):
                raise Exception('로그인 실패') 
            data['id'] = loginInfo['id']
            data['pw'] = loginInfo['pw']
            data['authority'] = str(member.authority)

            jwt_data = encode_jason_to_jwt(data)
            return_data = {'message' : '로그인 성공'}
            res = JsonResponse(return_data, status = 200)
            res.set_cookie('jwt', jwt_data)
            return res
        except Exception as e:
            return_data = {'memberInfo' : None, 'message' : '로그인 실패'}
            return JsonResponse(return_data, status=452)


# ==================================================================================================================================
#                                               회원 정보 검색 함수 모음
# ==================================================================================================================================

def admin_search_member(search_code,query):
    if query == '':
        return admin_read_all_info()
    code = {'아이디':0,"필명":1,"나이 (이상)":2, '나이 (이하)':3,'성별':4,'권한':5,'휴대폰 번호':6, '이메일':7}

    if code['아이디'] == search_code:
        datas = search_member_id(query)
        return JsonResponse(datas, status = 200)

    elif code['필명'] == search_code:
        print('필명')
        datas = search_member_nickname(query)
        return JsonResponse(datas, status = 200)

    elif code['나이 (이상)'] == search_code:
        datas = search_member_age_over(query)
        return JsonResponse(datas, status = 200)

    elif code['나이 (이하)'] == search_code:
        datas = search_member_age_under(query)
        return JsonResponse(datas, status = 200)

    elif code['성별'] == search_code:
        datas = search_member_gender(query)
        return JsonResponse(datas, status = 200)

    elif code['권한'] == search_code:
        datas = search_member_auth(query)
        return JsonResponse(datas, status = 200)

    elif code['휴대폰 번호'] == search_code:
        datas = search_member_phonenumber(query)
        return JsonResponse(datas, status = 200)    

    elif code['이메일'] == search_code:
        datas = search_member_email(query)
        return JsonResponse(datas, status = 200)  
    else:
        return JsonResponse({'message':'코드 에러\n잘못된 요청 코드입니다.'},status = 460)

def search_member_id(query):
    member = Member.objects.get(id__contains = query)
    data = {}
    data[0]=member.get_dic()
    return data


def search_member_nickname(query):
    member = Member.objects.get(nickname__contains = query)
    data = {}
    data[0]=member.get_dic()
    return data

def search_member_age_over(query):
    datas = {}
    members = Member.objects.filter(age__gte = query)
    index = len(members) - 1
    for member in members:
        datas[index]=member.get_dic()
        index -= 1
    return datas

def search_member_age_under(query):
    datas = {}
    members = Member.objects.filter(age__lte = query)
    index = len(members) - 1
    for member in members:
        datas[index]=member.get_dic()
        index -= 1
    return datas

def search_member_gender(query):
    datas = {}
    if query == '남성':
        members = Member.objects.filter(gender = True)
    elif query == '여성':
        members = Member.objects.filter(gender = False)
    else:
        members = Member.objects.filter(gender = query)
    index = len(members) - 1
    for member in members:
        datas[index]=member.get_dic()
        index -= 1
    return datas

def search_member_auth(query):
    datas = {}
    members = Member.objects.filter(authority = query)
    index = len(members) - 1
    for member in members:
        datas[index]=member.get_dic()
        index -= 1
    return datas

def search_member_phonenumber(query):
    datas = {}
    members = Member.objects.filter(phonenumber__contains = query)
    index = len(members) - 1
    for member in members:
        datas[index]=member.get_dic()
        index -= 1
    return datas

def search_member_email(query):
    datas = {}
    members = Member.objects.filter(email__contains = query)
    index = len(members) - 1
    for member in members:
        datas[index]=member.get_dic()
        index -= 1
    return datas

# ==================================================================================================================================
#                                               회원 정보 등록
# ==================================================================================================================================



# 회원가입
@csrf_exempt
def user_create_info(registInfo):
    data ={}
    # 회원가입 정보 검증 과정
    if isExist_id(registInfo['id']):
        return_data = {'message' : '이미 존재하는 아이디입니다.'}
        return JsonResponse(return_data, status = 453)
    
    if not isValid_nickname(registInfo['nickname']):
        return_data = {'message' : '이미 존재하는 닉네임입니다.'}
        return JsonResponse(return_data, status = 454)

    if not isValid_id(registInfo['id']):
        return_data = {'message' : '잘못된 아이디 형식입니다.'}
        return JsonResponse(return_data, status = 455)

    if not isValid_password(registInfo['pw']):
        return_data = {'message' : '잘못된 비밀번호 형식입니다.\n영문자,숫자,특수문자 포함 8~16자\n &나 | 제외'}
        return JsonResponse(return_data, status = 456)

    if not isValid_email(registInfo['email']):
        return_data = {'message' : '잘못된 이메일 형식입니다.'}
        return JsonResponse(return_data, status = 457)

    if not isValid_phonenumber(registInfo['phonenumber']):
        return_data = {'message' : '잘못된 전화번호 형식입니다.'}
        return JsonResponse(return_data, status = 458)

    # 회원가입 정보 등록 과정
    try:
        password = bcrypt.hashpw(registInfo['pw'].encode('utf-8'),bcrypt.gensalt())
        password = password.decode('utf-8')
        member = Member(id=registInfo['id'], pw=password, name=registInfo['name'], nickname=registInfo['nickname'], age=registInfo['age'],
                        gender=registInfo['gender'], authority=settings.AUTHORITY['회원'], phonenumber=registInfo['phonenumber'], email=registInfo['email'])
        member.save()
        data['id'] = member.id
        data['authority'] = settings.AUTHORITY['회원']
        print(settings.AUTHORITY['회원'])
        jwt_data = encode_jason_to_jwt(data)
        return_data = {'jwt': jwt_data, 'message': '회원가입 성공'}
        return JsonResponse(return_data, status=200)
    except Exception as e:
        print(e)
        return_data = {'message' : '회원가입 실패, 관리자에게 문의바랍니다.'}
        return JsonResponse(return_data, status=459)


def admin_create_info(registInfo):
    data ={}
    # 관리자등록 정보 검증 과정
    if isExist_id(registInfo['id']):
        return_data = {'message' : '이미 존재하는 아이디입니다.'}
        return JsonResponse(return_data, status = 453)
    
    if not isValid_nickname(registInfo['nickname']):
        return_data = {'message' : '이미 존재하는 닉네임입니다.'}
        return JsonResponse(return_data, status = 454)

    if not isValid_email(registInfo['email']):
        return_data = {'message' : '잘못된 이메일 형식입니다.'}
        return JsonResponse(return_data, status = 457)

    if not isValid_phonenumber(registInfo['phonenumber']):
        return_data = {'message' : '잘못된 전화번호 형식입니다.'}
        return JsonResponse(return_data, status = 458)

    # 관리자 정보 등록 과정
    try:
        password = bcrypt.hashpw(registInfo['pw'].encode('utf-8'),bcrypt.gensalt())
        password = password.decode('utf-8')
        member = Member(id=registInfo['id'], pw=password, name=registInfo['name'], nickname=registInfo['nickname'], age=registInfo['age'],
                        gender=registInfo['gender'], authority=settings.AUTHORITY['관리자'], phonenumber=registInfo['phonenumber'], email=registInfo['email'])
        member.save()
        data['id'] = member.id
        data['authority'] = settings.AUTHORITY['관리자']
        print(settings.AUTHORITY['관리자'])
        jwt_data = encode_jason_to_jwt(data)
        return_data = {'jwt': jwt_data, 'message': '관리자 등록 성공'}
        return JsonResponse(return_data, status=200)
    except Exception as e:
        print(e)
        return_data = {'message' : '관리자등록 실패'}
        return JsonResponse(return_data, status=459)



# ==================================================================================================================================
#                                               회원 정보 조회
# ==================================================================================================================================

@csrf_exempt
def user_read_info(member_info):
    memberInfo = Member.objects.get(id=member_info['id'])
    return JsonResponse(memberInfo.get_dic(), status=200)


def admin_read_all_info():
    datas = {}
    memberInfos = Member.objects.all()
    index = len(memberInfos) - 1
    for member in memberInfos:
        datas[index] = member.get_dic()
        index -= 1
    return JsonResponse(datas, status = 200)



# ==================================================================================================================================
#                                               회원 정보 수정
# ==================================================================================================================================


def user_update_info(member_info, newInfo):
    member = Member.objects.get(id = member_info['id'])
    
    if not isValid_email(newInfo['email']):
        return JsonResponse({'message': '잘못된 이메일 형식입니다.'},status=457)
    
    if not isValid_phonenumber(newInfo['phonenumber']):
        return JsonResponse({'message': '잘못된 전화번호 형식입니다.'},status=458)

    if member.nickname != newInfo['nickname']:
        if not isValid_nickname(newInfo['nickname']):
            return JsonResponse({'message': '사용 불가능한 닉네임입니다.'},status=454)
    


    member.name = newInfo['name']
    member.nickname = newInfo['nickname']
    member.email = newInfo['email']
    member.phonenumber = newInfo['phonenumber']
    member.age = newInfo['age']
    member.gender = newInfo['gender']
    member.save()
    return JsonResponse({'message':'회원정보 수정이 완료되었습니다.'}, status=200)

@csrf_exempt
def user_change_password(request):
    passwordInfo = json.loads(request.body.decode('utf-8'))
    before_password=passwordInfo['before'] 
    new_password=passwordInfo['after']

    member_info = get_member_info(request.COOKIES)
    member = Member.objects.get(id = member_info['id'])
    password = member.pw

    if not bcrypt.checkpw(before_password.encode('utf-8') ,password.encode('utf-8')):
        return JsonResponse({'message':'기존 비밀번호와 일치하지 않습니다.'},status = 463)
    
    password = bcrypt.hashpw(new_password.encode('utf-8'),bcrypt.gensalt())
    password = password.decode('utf-8')
    member.pw = password
    member.save()

    return JsonResponse({'message':'패스워드가 정상적으로 변경되었습니다.'},status = 200)

    
        
def admin_update_info(newInfo):
    try:
        member = Member.objects.get(id = newInfo['id'])

        if member.nickname != newInfo['nickname']:
            if not isValid_nickname(newInfo['nickname']):
                return JsonResponse({'message': '사용 불가능한 닉네임입니다.'},status=454)

        if not isValid_email(newInfo['email']):
            return JsonResponse({'message': '잘못된 이메일 형식입니다.'},status=457)
    
        if not isValid_phonenumber(newInfo['phonenumber']):
            return JsonResponse({'message': '잘못된 전화번호 형식입니다.'},status=458)

        if not newInfo['pw'] == member.pw:
            password = bcrypt.hashpw(newInfo['pw'].encode('utf-8'),bcrypt.gensalt())
            password = password.decode('utf-8')
            member.pw = password
        member.name = newInfo['name']
        member.nickname = newInfo['nickname']
        member.email = newInfo['email']
        member.phonenumber = newInfo['phonenumber']
        member.age = newInfo['age']
        member.gender = newInfo['gender']
        member.save()
        return JsonResponse({'message':'회원정보 수정이 완료되었습니다.'}, status=200)
    except:
        return JsonResponse({'message':'회원정보 수정에 실패하였습니다.'}, status=461)




# ==================================================================================================================================
#                                               회원 정보 삭제
# ==================================================================================================================================


def user_delete_info(member_info):
    member = Member.objects.get(id = member_info['id'])

    member.delete()
    return JsonResponse({'message':'회원정보가 삭제되었습니다.\n그동안 이용해주셔서 감사합니다.'}, status=200)


# 여러 사용자 삭제 가능하도록
def admin_delete_info(member_infos):
    for member_info in member_infos:
        member = Member.objects.get(id=member_info['id'])
        member.delete()

    return JsonResponse({'message':'선택한 회원정보가 삭제되었습니다.'},status=200)



# ==================================================================================================================================
#                                               회원 온도 관련 함수 모음
# ==================================================================================================================================

def user_sementic_process(request):
    if request.method == 'GET':
        memberInfo = get_member_info(request.COOKIES)
        code = int(json.loads(request.GET.get('code')))
        return user_read_sementic(memberInfo, code)

    elif request.method == 'POST':
        memberInfo = get_member_info(request.COOKIES)
        sementicInfo = json.loads(request.body.decode('utf-8'))
        return user_create_sementic_initial(memberInfo,sementicInfo)



# 하루 처음 접속시 초기 감정값 결정하는 함수
def user_create_sementic_initial(memberInfo,sementicInfo):
    sementic_code ={'0':36.5, '1':28, '2':32, '3':36.5, '4':38, '5':42}
    member = Member.objects.get(id = memberInfo['id'])
    senti = SementicRecord(member=member, initial_value=sementic_code[sementicInfo['code']],current_temperature=sementic_code[sementicInfo['code']])
    senti.save()
    return JsonResponse({'message': '정상적으로 저장되었습니다.'},status = 200)


# 사용자의 감정내역 조회 처리 함수
def user_read_sementic(memberInfo, temp_code):
    code ={'당일':0, '최근일주일':1,'최근한달':2}

    if code['당일'] == temp_code:
        datas = user_read_sementic_for_today(memberInfo)
        return JsonResponse(datas, status = 200)
        
    elif code['최근일주일'] == temp_code:
        datas = user_read_sementic_for_week(memberInfo)
        return JsonResponse(datas, status = 200)

    elif code['최근한달'] == temp_code:
        datas = user_read_sementic_for_month(memberInfo)
        return JsonResponse(datas, status = 200)


# 최근 일주일간의 감정지수를 조회하는 함수
def user_read_sementic_for_week(memberInfo):
    datas = {}
    member = Member.objects.get(id=memberInfo['id'])
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    senti_records = SementicRecord.objects.filter(date__lte = datetime.date.today(), date__gte=last_week,member = member)
    index = len(senti_records) - 1
    for senti_record in senti_records:
        datas[index] = senti_record.get_dic()
        index -= 1
    return datas

# 최근 한달의 감정지수를 조회하는 함수
def user_read_sementic_for_month(memberInfo):
    datas = {}
    member = Member.objects.get(id=memberInfo['id'])
    last_week = datetime.date.today() - relativedelta(months = 1)
    senti_records = SementicRecord.objects.filter(date__lte = datetime.date.today(), date__gte=last_week,member = member)
    index = len(senti_records) - 1
    for senti_record in senti_records:
        datas[index] = senti_record.get_dic()
        index -= 1
    return datas

# 오늘의 감정지수를 조회하는 함수
def user_read_sementic_for_today(memberInfo):
    member = Member.objects.get(id=memberInfo['id'])
    senti_records = SementicRecord.objects.get(date = datetime.date.today(), member = member)
    return senti_records.get_dic()


# ==================================================================================================================================
#                                               검증 함수 모음
# ==================================================================================================================================

# 사용 가능한 ID 인지 확인
def isExist_id(id):
    if  Member.objects.filter(id=id).exists():
        return True
    else:
        return False


# 아이디에 특수문자가 입력된 경우 False를 반환
def isValid_id(id):
    idCheck1 = re.compile("[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]")
    idCheck2 = re.compile('[a-zA-Z0-9]{8,20}')
    if idCheck1.match(id):
        return False
    else:
        if not idCheck2.match(id):
            return False
        else:
            return True

def isValid_password(password):
    passwordCheck = re.compile('^(?=.*[a-zA-Z])(?=.*[!@#$%^~*+=-])(?=.*[0-9]).{8,16}$')
    if not passwordCheck.match(password):
        return False
    else:
        return True


def isValid_email(email):
    emailCheck = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not emailCheck.match(email):
        return False
    else:
        return True

def isValid_phonenumber(phoneNumber):
    phoneNumberCheck =re.compile('[0-9]{2,3}-[0-9]{3,4}-[0-9]{4,4}')
    if not phoneNumberCheck.match(phoneNumber):
        return False
    else:
        return True

def isValid_nickname(nickname):
    if Member.objects.filter(nickname=nickname).exists():
        return False
    else:
        return True