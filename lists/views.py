#Created 2-6-15 Steffan
from django.shortcuts import render, redirect
from django.http import HttpResponse
#from lists.models import Item, List

# Create your views here.
#Example view below
def home_page(request):
    return render(request, 'home.html')

def organization_sign_up(request):
	return render(request, 'organization.html')

def user_sign_up(request):
	return render(request, 'user.html')
	
def footer(request):
	return render(request, 'footer.html')
	
def header(request):
	return render(request, 'header.html')