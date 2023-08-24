from django.db import models
from User import models as Umodels
# Create your models here.

class Liveroom(models.Model):
    roomID = models.AutoField(primary_key=True,verbose_name="roomID")
    roomName = models.CharField(max_length=100,blank=False,null=False,verbose_name="roomName")
    roomInfo = models.CharField(max_length=2048,verbose_name="roomInfo")
    roomcover = models.ImageField(upload_to="livecover/",verbose_name="roomcover")
    roomstatus = models.BooleanField(default=False,verbose_name="roomstatus")
    Owner = models.ForeignKey(Umodels.User, on_delete=models.CASCADE, verbose_name="Owner")

    def __str__(self):
        return self.roomName
    class Meta:
        db_table = "直播间表"


