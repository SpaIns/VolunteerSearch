#Created 2-6-15 Steffan
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from lists.models import User, Position, Skill
from lists.admin import UserCreationForm, OrgCreationForm, JobCreationForm, UserUpdateProfile, OrgUpdateProfile, FillPosition

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

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/accounts/register/complete')

    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'registration/registration_form.html', token)

def org_register(request):
    if request.method == 'POST':
        form = OrgCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/accounts/register/complete')

    else:
        form = OrgCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'registration/org_registration_form.html', token)

def job_create(request):
    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.parent = request.user
            new_user.save()
            return HttpResponseRedirect('/accounts/profile')#NEED TO CHANGE THIS

    else:
        data = {'parent': request.user}
        form = JobCreationForm(initial=data)
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'registration/job_creation_form.html', token)
	
def registration_complete(request):
    return render(request, 'registration/registration_complete.html')

def user_profile(request):
    jobs = Position.objects.filter(parent=request.user)
    myjobs = Position.objects.filter(child=request.user)
    if request.method == 'POST':
        form = FillPosition(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile')
    else:
        form = FillPosition()

    return render(request, 'profile/userprofile.html', {'jobs': jobs, 'myjobs': myjobs, 'form': form})
	
def org_profile(request):
	return render(request, 'profile/orgprofile.html')
	
def job_view(request):
	if (request.GET.get('officebutton')):
		jobs = Position.objects.filter(skills__skill = 'ms_office')	
	else:
		jobs = Position.objects.all()
    
	return render(request, 'profile/jobview.html', {'jobs': jobs})

def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UserUpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile')
    else:
        data = {'email' : request.user.email, 'date_of_birth' : request.user.date_of_birth, 'location_city' : request.user.location_city, 'location_state' : request.user.location_state, 'age' : request.user.age, 'bio' : request.user.bio, 'skill' : request.user.skill.all()}
        form = UserUpdateProfile(initial=data)

    args['form'] = form
    return render(request, 'registration/update_profile.html', args)

def update_org_profile(request):
    args = {}

    if request.method == 'POST':
        form = OrgUpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile')
    else:
        data = {'email' : request.user.email, 'location_city' : request.user.location_city, 'location_state' : request.user.location_state, 'bio' : request.user.bio}
        form = OrgUpdateProfile(initial=data)

    args['form'] = form
    return render(request, 'registration/update_org_profile.html', args)