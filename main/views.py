from django.shortcuts import render
from User.models import User
from video.models import Video,Classification
from User import views as userview
from livechat.models import Liveroom
# Create your views here.
def test(request):

    try:
        userid = request.session.get('UserID', None)
        user = User.objects.filter(User_ID=userid).first()
    except:
        user = None
    classlist = Classification.objects.filter()
    if request.method== 'POST':
        print("ssssssssssssssssssssssss")
        classcode=request.POST.get("class")
        classs=Classification.objects.filter(Ccode=classcode).first()
        videlist=Video.objects.filter(Classification=classs)
        return render(request, 'index.html', {'videolist': videlist,
                                              'user': user,
                                              'classlist': classlist, })

    videlist=Video.objects.filter()
    return render(request, 'index.html',{'videolist':videlist,
                                         'user':user,
                                         'classlist':classlist,})

def Livelist(request):
    try:
        userid = request.session.get('UserID', None)
        user = User.objects.filter(User_ID=userid).first()
    except:
        user = None


    livelist=Liveroom.objects.filter()


    return render(request, 'livelist.html',{'livelist':livelist,
                                         'user':user,
                                         })

