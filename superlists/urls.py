#Created 2-6-15 Steffan
#added footer,header,org,user, home links 2-24-16 Steffan
"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from lists import views as list_views
from lists import urls as list_urls

urlpatterns = [
#examples below
    url(r'^$', list_views.home_page, name='home'),
    #url(r'^lists/', include(list_urls)),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^usersignup/', list_views.user_sign_up, name='userSignUp'),
	url(r'^organizationsignup/', list_views.organization_sign_up, name='orgSignUp'),
	url(r'^footer/', list_views.footer, name='footer'),
	url(r'^header/', list_views.header, name='header'),
]
