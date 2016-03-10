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
    
def about(request):
    return render(request, 'about.html')

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
    jobs = Position.objects.all()	
    if (request.GET.get('officebutton')):
        jobs = Position.objects.filter(skills__skill = 'MS Office')
    if (request.GET.get('codebutton')):
        jobs = Position.objects.filter(skills__skill = 'Programming')
    if (request.GET.get('srhelpbutton')):
        jobs = Position.objects.filter(skills__skill = 'Senior Help')	
    if (request.GET.get('groomingbutton')):
        jobs = Position.objects.filter(skills__skill = 'Pet Grooming')	
    if (request.GET.get('walkingbutton')):
        jobs = Position.objects.filter(skills__skill = 'Dog Walking')	
    if (request.GET.get('trainingbutton')):
        jobs = Position.objects.filter(skills__skill = 'Pet Training')	
    if (request.GET.get('tutoringbutton')):
        jobs = Position.objects.filter(skills__skill = 'Tutoring')	
    if (request.GET.get('constructionbutton')):
        jobs = Position.objects.filter(skills__skill = 'Construction')	
    if (request.GET.get('restorationbutton')):
        jobs = Position.objects.filter(skills__skill = 'Restoration')	
    if (request.GET.get('landscapingbutton')):
        jobs = Position.objects.filter(skills__skill = 'Landscaping')	
    if (request.GET.get('liftingbutton')):
        jobs = Position.objects.filter(skills__skill = 'Heavy Lifting')
    if (request.GET.get('clearbutton')):
        jobs = Position.objects.all()
    
    return render(request, 'profile/jobview.html', {'jobs': jobs})

def profile_search(request):
    query = User.objects.all()
    users = list()
    orgs = list()
    if (request.GET.get('profsearchbutton')):
        query = User.objects.filter(user_name = request.GET.get('profsearchbox'))
    for profile in query:
        if profile.user_type == 'USER':
            users.append(profile)
        else:
            orgs.append(profile)

    return render(request, 'profile/search.html', {'users': users, 'orgs': orgs})

def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UserUpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile')
    else:
        data = {'email' : request.user.email, 'date_of_birth' : request.user.date_of_birth, 'location_city' : request.user.location_city, 'location_state' : request.user.location_state, 'age' : request.user.age, 'bio' : request.user.bio, 'skills' : request.user.skills.all()}
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
