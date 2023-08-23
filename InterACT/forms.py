from django import forms

from .models import Comment_Table

class CommentForm(forms.ModelForm):
    Comment = forms.CharField(error_messages={'required': '不能为空',},
        widget=forms.Textarea(attrs = {'placeholder': '请输入评论内容' },)
    )

    class Meta:
        model = Comment_Table
        fields = ['Comment']
        label={'Comment':'评论',}
