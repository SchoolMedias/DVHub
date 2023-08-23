"""DVhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
import InterACT.views as IACT
import User.views
import main.views
import video.views
import livechat.views
from video import views
import livechat.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('Register/',User.views.Register,name='register'),
    path('',main.views.test,name='index'),
    path('login/',User.views.signin,name='login'),
    path('logout/',User.views.logout,name='logout'),
    path('user',User.views.UserPage,name='user'),
    path('vupload/',views.vupload,name='upload'),
    path('fans/', User.views.fans, name='fans'),
    path('interest/', User.views.interest, name='interest'),
    path('comment/',IACT.comment),
    #登记函数
    path('commentChangeStatus',IACT.commentChangeStatus),
    path('commentEdit',IACT.commentEdit),
    path('commentDelete',IACT.commentDelete),
    path('vmodify/<int:dvcode>', views.vmodify, name='modify'),
    path('vplay/<int:dvcode>', views.vplay, name='vplay'),
    path('profile/',User.views.profile,name='profile'),
    path('password/',User.views.password,name='password'),
    path('imgcenter/',User.views.imgcenter,name='imgcenter'),
    path("livefile", livechat.views.roomfile, name="livefile"),
    #api
    path('api/danmu',video.views.gdanmu),

    path('chat/', include('livechat.urls')),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




