

from django.shortcuts import render,HttpResponse,redirect
import User.models as Usermodels
from .forms import LiveForm
from User.views import islogin
from .models import Liveroom

def chatroom(request):
    return render(request, 'chatroom.html')


def room(request, room_name):
    userid = request.session.get('UserID', None)
    user = Usermodels.User.objects.filter(User_ID=userid).first()
    tliveroom = Liveroom.objects.filter(roomID=room_name).first()
    if request.method == 'GET':
        if islogin(request) == False:
            return redirect('/login')



    if request.method == 'POST':
        print(request.POST.get('flag'))

        if request.POST.get('flag') == '开始直播':
            tliveroom.roomstatus = True
        elif request.POST.get('flag') == '结束直播':
            tliveroom.roomstatus = False
        tliveroom.save()

    content={
        "room":tliveroom,
        "user":user,
            }
    return render(request, "room.html", content)



def roomfile(request):
    if islogin(request) == False:
        return redirect('/login')
    userid=request.session.get('UserID', None)
    user=Usermodels.User.objects.filter(User_ID=userid).first()
    liveroom=Liveroom.objects.filter(Owner=user).first()
    form = LiveForm(instance=liveroom, data=request.POST, files=request.FILES)
    if request.method == 'POST':
        if not liveroom:
            if form.is_valid():
                tliveroom=Liveroom()
                tliveroom.roomName=request.POST.get("roomName")
                tliveroom.roomInfo = request.POST.get("roomInfo")
                tliveroom.roomcover = request.FILES.get("roomcover")
                tliveroom.Owner = user
                tliveroom.save()
        else:
            if form.is_valid():
                form.save()
    if request.method == 'GET':
        # if not liveroom:
        #     form = LiveForm()
        # else:
            form = LiveForm(instance=liveroom)

    content={
        "user":user,
        "form":form,
        "id":liveroom.roomID,
            }
    return render(request, "livefile.html", content)

