from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['status', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
