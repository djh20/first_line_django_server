from django.shortcuts import render
from .models import Report
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from member.models import Member
from member.jwt_manager import get_member_info
from post.models import Post
from reply.models import Reply
from django.utils import timezone
# Create your views here.
rowsPerPage = 20

@csrf_exempt 
def process_admin_report(request):
    if request.method == "GET":
        return process_admin_read(request)
    # if request.method == "POST":
    #     return process_admin_create(request)
    return JsonResponse({'message' : "존재하지 않는 요청"})



def get_reports_by_report_id(request, query):
    reports = Report.objects.filter(report_id = query)
    return reports
def get_reports_by_report_text(request, query):
    reports = Report.objects.filter(report_text__icontains = query)
    return reports
def get_reports_by_process_text(request, query):
    reports = Report.objects.filter(process_text__icontains = query)
    return reports
def get_reports_by_report_date_upper(request, query):
    reports = Report.objects.filter(report_date__gte = query)
    return reports
def get_reports_by_report_date_lower(request, query):
    reports = Report.objects.filter(report_date__lte = query)
    return reports
def get_reports_by_process_date_upper(request, query):
    reports = Report.objects.filter(process_date__gte = query)
    return reports
def get_reports_by_process_date_lower(request, query):
    reports = Report.objects.filter(process_date__lte = query)
    return reports
def get_reports_by_report_writer(request, query):
    reports = Report.objects.filter(report_writer = query)
    return reports
    
def get_reports_by_process_writer(request, query):
    reports = Report.objects.filter(process_writer = query)
    return reports
def get_reports_by_is_processed(request, query):
    reports = Report.objects.filter(is_processed = query)
    return reports
def get_reports_by_post(request, query):
    reports = Report.objects.filter(post = query)
    return reports
def get_reports_by_reply(request, query):
    reports = Report.objects.filter(reply = query)
    return reports
 
def get_reports_by_process_type(request, query):
    reports = Report.objects.filter(process_type = query)
    return reports

def process_admin_read(request):
    condition_dic = {
    "신고 번호" : get_reports_by_report_id,
    "신고 내용" : get_reports_by_report_text,
    "처리 결과" : get_reports_by_process_type,
    "처리 내용" : get_reports_by_process_text,
    "신고일(이상)" : get_reports_by_report_date_upper,
    "신고일(이하)" : get_reports_by_report_date_lower,
    "처리일(이상)" : get_reports_by_process_date_upper,
    "처리일(이하)" : get_reports_by_process_date_lower,
    "신고자" : get_reports_by_report_writer,
    "처리자" : get_reports_by_process_writer,
    "처리 여부" : get_reports_by_is_processed,
    "대상 게시글 ID" : get_reports_by_post,
    "대상 댓글 ID" : get_reports_by_reply,
    }
    function = condition_dic[request.GET.get('condition')]
    query = request.GET.get('query')
    reports = function(request, query)
    print(reports)
    data = {}
    idx = 0
    for report in reports:
        data[idx] = report.get_for_admin()
        idx+=1
    print(data)
    return JsonResponse({'data' : data})

def read_report(request, pk):
    if request.method == "GET":
        report = Report.objects.filter(report_id = pk).first()
        return JsonResponse({'data' : report.get_for_admin()})

@csrf_exempt 
def process_report(request):
    if request.method == "POST":
        try :
            report_info = json.loads(request.body.decode('utf-8'))

            report_id = report_info['report_id']
            process_text = report_info['process_text']
            process_type = report_info['process_type']
            process_writer = Member.objects.get(id = get_member_info(request.COOKIES)['id'])

            report = Report.objects.filter(report_id = report_id).first()
            reported = report.get_reported()
            if process_type == "블라인드" : 
                reported.is_blinded = True
            elif process_type == "삭제" : 
                reported.is_deleted = True
            reported.save()
            report.process_type = process_type
            report.process_writer = process_writer
            report.process_text = process_text
            report.process_date = timezone.now()
            report.is_processed = True

            report.save()
            return JsonResponse({'message' : "성공적으로 삭제되었습니다"}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message' : "처리에 실패했습니다"}, status=400)


        