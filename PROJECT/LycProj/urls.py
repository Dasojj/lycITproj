from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from Diary import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('register', views.RegisterFormView.as_view()),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path(r'captcha/', include('captcha.urls')),
    path('newnotebig', views.makenewbignote),
    path('eventreg', views.makeneweventnote),
    path('newnotelittle', views.makenewlittlenote),
    path('bignotelist', views.viewbignotes),
    path('bignotelistdel', views.deletebignotes),
    path('bignotelistred', views.redactbignotes),
    path('littlenotelist', views.viewlittlenotes),
    path('littlenotelistdel', views.deletelittlenotes),
    path('littlenotelistred', views.redactlittlenotes),
    path('eventnotelist', views.vieweventnotes),
    path('eventnotelistdel', views.deleteeventnotes),
    path('eventnotelistred', views.redacteventnotes),
    path('bignoteview', views.viewbignote),
    path('bignoteredact', views.redactbignote),
    path('bignotedelete', views.deletebignote),
    path('littlenoteview', views.viewlittlenote),
    path('littlenoteredact', views.redactlittlenote),
    path('littlenotedelete', views.deletelittlenote),
    path('eventnoteview', views.vieweventnote),
    path('eventnoteredact', views.redacteventnote),
    path('eventnotedelete', views.deleteeventnote),
    path('reverse', views.revmail),
    path('importlittlenote', views.importlittlenote),
    path('importbignote', views.importbignote),
    path('moodnotelist', views.viewmoodnotes),
    path('moodnotelistdel', views.deletemoodnotes),
    path('moodnoteview', views.viewmoodnote),
    path('moodreg', views.makenewmoodnote),
    path('profilesettings', views.profilesettings),
    path('', views.MainPage),
    path('getstatpng', views.showstats),
    path('statistics', views.rendstats),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()