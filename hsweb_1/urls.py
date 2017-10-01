"""hsweb_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def index(request):
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        user = None
    return render(request, 'index.html', {'user': user})
    

def login(request):
    user = None
    print(request.user)
    if request.POST:
        username = request.POST.get('user')
        pword = request.POST.get('pword')
        user = authenticate(username=username, password=pword)
        if user is not None:
            auth_login(request, user)
    return render(request, 'login.html', {'user': user})
    

urlpatterns = [
    # api 
    url(r'^api/locations/', include('locations.api.urls')),
    url(r'^api/phones/', include('phones.api.urls')),
    url(r'^api/issues/', include('issues.api.urls')),
    url(r'^api/kits/', include('cdks.api.urls')),
    url(r'^api/devices/', include('devices.api.urls')),
    # html 
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^cdks/', include('cdks.urls')),
    url(r'^devices/', include('devices.urls')),
    url(r'^issues/', include('issues.urls')),
    url(r'login/', login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^$', index, name='home'),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
