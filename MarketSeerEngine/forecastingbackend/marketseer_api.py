from django.shortcuts import render
from django.http import HttpResponse

def datarequest(request):
	return HttpResponse("checking this works")