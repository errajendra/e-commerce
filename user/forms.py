from typing import Any
from django import forms
from .models import CustomUser as User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'dialing_code', 'mobile_number', )
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dialing_code': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
