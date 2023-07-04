from django.shortcuts import render
from User.models import User
from video.models import Video,Classification
from User import views as userview
# Create your views here.
def test(request):

    try:
        userid = request.session.get('UserID', None)
        user = User.objects.filter(User_ID=userid).first()
    except:
        user = None

    videlist=Video.objects.filter()
    classlist=Classification.objects.filter()
    print(request.GET.get('class'))



    return render(request, 'index.html',{'videolist':videlist,
                                         'user':user,
                                         'classlist':classlist,})
