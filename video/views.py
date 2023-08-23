from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.http import require_http_methods

from .forms import VideoForm
from .models import Video,User,Classification
from User.views import islogin
from InterACT import models as Intermodels
from InterACT import forms
from django.http import JsonResponse
# Create your views here.

def vupload(request):
    if islogin(request) == False:
        return redirect('/login')
    userid = request.session.get('UserID', None)
    user = User.objects.filter(User_ID=userid).first()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        tuserid=request.session.get('UserID', None)
        tuser=User.objects.filter(User_ID=tuserid).first()
        if form.is_valid():
            tmodel = Video()
            tmodel.Title = request.POST.get('Title')
            tmodel.Content = request.POST.get('Content')
            tCcode = request.POST.get('Classification')
            tClassification=Classification.objects.filter(Ccode=tCcode).first()
            tmodel.Classification = tClassification
            tmodel.User = tuser
            tmodel.VideoFile = request.FILES.get('VideoFile')
            tmodel.CoverFile = request.FILES.get('CoverFile')
            tmodel.save()
        else:
            print("wrong")
        return redirect('/vupload/')
    else:
        if not (request.session.get('is_login', None) == True):
            return redirect('/login')
        form = VideoForm()
        return render(request,"upload.html",{'form':form,
                                             'user':user})
    

def vmodify(request,dvcode):
    if islogin(request) == False:
        return redirect('/login')
    userid = request.session.get('UserID', None)
    user = User.objects.filter(User_ID=userid).first()
    tvideo=Video.objects.filter(DVcode=dvcode).first()
    if tvideo is None:
        return render(request,"wrong/NosuchFile.html")
    if request.method == 'POST':
        print('herep')
        if request.POST.get('delete') == 'yes':
            print('here')
            tvideo.delete()
            return render(request,"wrong/NosuchFile.html")
        form = VideoForm(instance=tvideo, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        
    if request.method == 'GET':
        form = VideoForm(instance=tvideo)
    return render(request,"modify.html",{'form':form,
                                         'user':user})

def vplay(request,dvcode):
    tvideo = Video.objects.filter(DVcode=dvcode).first()
    userid = request.session.get('UserID', None)
    user = User.objects.filter(User_ID=userid).first()
    likeCount = Intermodels.Like_Favorite_Table.objects.filter(Type="like", DV=tvideo).count()

    # 收藏数量
    favorite = Intermodels.Like_Favorite_Table.objects.filter(Type="favorite", DV=tvideo).count()

    #评论列表
    commentlist = Intermodels.Comment_Table.objects.filter(DV=tvideo)

    # 是否点赞
    likeRow = Intermodels.Like_Favorite_Table.objects.filter(Type="like", User=user, DV=tvideo).first()

    # 是否收藏
    favoriteRow = Intermodels.Like_Favorite_Table.objects.filter(Type="favorite", User=user, DV=tvideo).first()
    form=forms.CommentForm

    # 是否关注
    interest = Intermodels.Attention_Table.objects.filter(User=user,Up=tvideo.User).first()


    likelist =[]
    for lik in Intermodels.Attention_Table.objects.filter(User=user):
        likelist.append(lik.Up)
    if request.method == 'POST':
        if islogin(request) == False:
            return redirect('/login')
        if request.POST.get('good')=='yes':
            interact = Intermodels.Like_Favorite_Table()
            userid = request.session.get('UserID', None)
            user = User.objects.filter(User_ID=userid).first()
            interact.User=user
            interact.DV=tvideo
            interact.Type='like'
            interact.save()
        if request.POST.get('like')=='yes':
            interact = Intermodels.Like_Favorite_Table()
            if islogin(request) == False:
                return redirect('/login')
            userid = request.session.get('UserID', None)
            user = User.objects.filter(User_ID=userid).first()
            interact.User=user
            interact.DV=tvideo
            interact.Type='favorite'
            interact.save()
        if request.POST.get('comment')=='yes':
            comment=request.POST.get('Comment')
            commentact=Intermodels.Comment_Table()
            commentact.Comment=comment
            commentact.User=user
            commentact.DV=tvideo
            commentact.save()
        if request.POST.get('addinterest')=='yes':
            addusr=request.POST.get('userid')
            addusr=User.objects.filter(User_ID=addusr).first()
            fanitem=Intermodels.Attention_Table()
            fanitem.User=user
            fanitem.Up=addusr
            if fanitem not in likelist:
                fanitem.save()
        if request.POST.get('cancelinterest')=='yes':
            cancelusr=request.POST.get('userid')
            canusr=User.objects.filter(User_ID=cancelusr).first()
            fanitem=Intermodels.Attention_Table.objects.filter(User=user,Up=canusr).first()
            fanitem.delete()


        return redirect('vplay',dvcode)

    if request.method == 'GET':
        tvideo.Viewsnum+=1
        tvideo.save()
        return render(request,"play.html",{
            'video':tvideo,
            'goods': likeCount,
            'likes': favorite,
            'likeRow': likeRow,
            'favoriteRow': favoriteRow,
            'commentlist': commentlist,
            'form':form,
            'user':user,
            'interest':interest,
        })

def getvalue(a):
    return a
@require_http_methods(["GET"])
def gdanmu(request):
    data={
        'code': 0,
        'data':[
           # [  ],
            [   2.11120,
                0,
                16777215,
                "sadas",
                "你好",
            ],
            [ 3.11120,
             0,
             16777215,
             "sadas",
             "你好",
             ],
            [5.0,
             0,
             16777215,
             "sadas",
             "你好",
             ]
        ]
    }
    print(data['data'][0][2])
    return JsonResponse(data)