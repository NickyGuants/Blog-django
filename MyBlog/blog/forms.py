from . models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=25)
    #email=forms.EmailField()
    receipient=forms.EmailField()
    comments=forms.CharField(required=False, widget=forms.Textarea)