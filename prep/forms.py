from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['full_name', 'phone', 'bio', 'photo']
		widgets = {
			'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
			'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
			'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write something about yourself'}),
			'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
		}
