from django import forms
from blog.models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','body']
        exclude = ('create_timestamp','is_delete','last_edit_timestamp')
        widgets = {'body':forms.Textarea(attrs={'rows':10,'cols':60})}
