from django.shortcuts import render
from .models import Notice
from django.http import JsonResponse
# Create your views here.
def admin_search_notice(request):
    notices = Notice.objects.all()
    data = {}
    idx = 0
    for notice in notices:
        data[idx] = notice.get_for_admin()
        idx+=1
    return JsonResponse(data)
