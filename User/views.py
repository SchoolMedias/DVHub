import datetime

from django.shortcuts import render,HttpResponse,redirect
from .forms import RegisterForm,EditProfileForm
from User import models
from video.models import Video
from django.utils import timezone
import pytz
from InterACT.models import Attention_Table
from django.http import JsonResponse
tz = pytz.timezone('Asia/Shanghai')
# Create your views here.
def Register(request):
    status = 0
    print(RegisterForm)
    userid = request.session.get('UserID', None)
    user = models.User.objects.filter(User_ID=userid).first()
    if (request.method=="POST") :
        try:
            print(request.FILES)
            md1=models.User()
            md1.NickName=request.POST.get('NickName')
            md1.Password=request.POST.get('Password')
            md1.Email=request.POST.get('Email')
            md1.Phone_number=request.POST.get('Phone_number')
            md1.Profile_photo=request.FILES.get('Profile_photo')
            if models.User.objects.filter(Email=md1.Email).first() is None:
                print("23456787654reqwrwqeqw")
                print(request.FILES.get('Profile_photo'))
                md1.Background_photo=request.FILES.get('Profile_photo')
                now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
                now = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
                md1.Register_time=now
                md1.save()
                print(str(md1.User_ID))
                status=1
                return redirect('/login')
                #print(request.POST.get('Stu_Department'))
            else:
                status=2
             #   return JsonResponse({'status':status})
        except:
            status=0
            #return JsonResponse({'status': status})

    return render(request,'regist.html',{
                                            'user':user,
                                            'status':status
                                            })


def UserPage(request):
    if islogin(request) == False:
        return redirect('/login')
    userid=request.session.get('UserID', None)
    user=models.User.objects.filter(User_ID=userid).first()
    videlist = Video.objects.filter(User=user)

    return render(request,'author.html',{'user':user,
                                         'videolist':videlist})

def islogin(request):
    if not (request.session.get('is_login', None) == True):
        print(666)
        return False
    else:
        return True
def signin(request):
    if islogin(request) == True:
        return redirect('/user')
    if (request.method == "POST"):
        Useremail=request.POST.get('email')
        Userpassword=request.POST.get('password')
        try:
            user=models.User.objects.filter(Email=Useremail).first()
            if user.Password == Userpassword:
                request.session['is_login']=True
                request.session['UserID']=user.User_ID
                print('true')
                return redirect('/user')
        except:
                print('无此邮箱')
    return render(request, 'signin.html')

def profile(request):
    if islogin(request) == False:
        return redirect('/login')
    userid = request.session.get('UserID', None)
    user = models.User.objects.filter(User_ID=userid).first()
    if request.method == 'POST':
        form = EditProfileForm(instance=user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
    if request.method == 'GET':
        form = EditProfileForm(instance=user)
    return render(request, 'profile.html',{'user':user,
                                           'form':form
                                           })

def password(request):
    if islogin(request) == False:
        return redirect('/login')
    userid = request.session.get('UserID', None)
    user = models.User.objects.filter(User_ID=userid).first()
    if request.method == 'POST':
        pwd=request.POST.get('pswd')
        user.Password=pwd
        user.save()

    return render(request, 'password.html',{'user':user}
                  )

def imgcenter(request):
    if islogin(request) == False:
        return redirect('/login')
    userid = request.session.get('UserID', None)
    user = models.User.objects.filter(User_ID=userid).first()
    videos = Video.objects.filter(User=user)

    return render(request, 'imgcenter.html',{'user':user,
                                             'videos':videos}
                  )


def fans(request):
    if islogin(request) == False:
        return redirect('/login')
    userid = request.session.get('UserID', None)
    user = models.User.objects.filter(User_ID=userid).first()
    fanslist = Attention_Table.objects.filter(Up=user)
    likelist =[]
    for lik in Attention_Table.objects.filter(User=user):
        likelist.append(lik.Up)
    fanlikes = []
    for fans in fanslist:
        if fans.User in likelist:
            fanlikes.append((fans,True))
        else:
            fanlikes.append((fans, False))
    if request.method=='POST':
        if request.POST.get('addinterest')=='yes':
            addusr=request.POST.get('userid')
            addusr=models.User.objects.filter(User_ID=addusr).first()
            fanitem=Attention_Table()
            fanitem.User=user
            fanitem.Up=addusr
            if fanitem not in likelist:
                fanitem.save()
        if request.POST.get('cancelinterest')=='yes':
            cancelusr=request.POST.get('userid')
            canusr=models.User.objects.filter(User_ID=cancelusr).first()
            fanitem=Attention_Table.objects.filter(User=user,Up=canusr).first()
            fanitem.delete()
        return redirect('/fans')
    return render(request, 'fans.html', {'user': user,
                                         'fanslist': fanlikes,
                                         }
                  )

def interest(request):
    if islogin(request) == False:
        return redirect('/login')
    userid = request.session.get('UserID', None)
    user = models.User.objects.filter(User_ID=userid).first()
    fanslist=Attention_Table.objects.filter(User=user)
    if request.method=='POST':
        if request.POST.get('cancelinterest')=='yes':
            cancelusr=request.POST.get('userid')
            canusr=models.User.objects.filter(User_ID=cancelusr).first()
            fanitem=Attention_Table.objects.filter(User=user,Up=canusr).first()
            fanitem.delete()
        return redirect('/interest')
    return render(request, 'interest.html', {'user': user,
                                         'userslist': fanslist,}
                  )




def logout(request):
    if not request.session.get('is_login', None):  # logout就是刷新session,即清空了登录信息，然后再跳转到login
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login")


