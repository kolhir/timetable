"""vpitt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from timetable import views as tt_views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('get_room',  tt_views.get_room),
    path('get_teacher',  tt_views.get_teacher),
    path('timetable/done',  tt_views.timetable_done),
    path('fill_profile/post/',  tt_views.fill_profile_post),
    path('fill_profile/',  tt_views.fill_profile),
    path('timetable/', tt_views.table_view),
    path('', tt_views.base_view),
    path("save_changes", tt_views.post),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
