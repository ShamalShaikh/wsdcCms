from django import forms
from .models import Questions, Answers

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Answers
		fields = ('question','answer')