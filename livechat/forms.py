from django import forms
from .models import Liveroom

class LiveForm(forms.ModelForm):
    class Meta:
        model = Liveroom
        fields = ["roomName","roomInfo","roomcover"]
        labels = {"roomName":'房间名',"roomInfo":'直播简介',"roomcover":'封面',}
