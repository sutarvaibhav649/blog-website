from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'placeholder':'leave you comment here....',
                'row':3,
                'class':'form-control'
            }
        )
    )
    class Meta:
        model = Comment
        fields = ['content']
    