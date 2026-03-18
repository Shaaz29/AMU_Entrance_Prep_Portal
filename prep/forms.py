from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['full_name', 'phone', 'bio', 'photo', 'photo_position_x', 'photo_position_y']
		widgets = {
			'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
			'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
			'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write something about yourself'}),
			'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
			'photo_position_x': forms.HiddenInput(),
			'photo_position_y': forms.HiddenInput(),
		}

	def clean_photo(self):
		photo = self.cleaned_data.get('photo')
		if photo:
			# Check file size (max 5MB)
			if photo.size > 5 * 1024 * 1024:
				raise ValidationError('Image file size must not exceed 5MB.')
			
			# Check file extension
			allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
			file_name = photo.name.lower()
			file_extension = file_name.split('.')[-1] if '.' in file_name else ''
			
			if file_extension not in allowed_extensions:
				raise ValidationError(
					f'Invalid file type. Allowed formats: {", ".join(allowed_extensions.upper())}.'
				)
		
		return photo
