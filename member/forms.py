from django import forms
from .models import Member
class LoginForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['id','pw']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})