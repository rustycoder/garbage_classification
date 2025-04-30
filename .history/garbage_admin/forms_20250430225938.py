from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from garbage_admin.models import Profile, TokenTransaction
from django.forms import ModelForm
from django import forms


class SignUpForm(UserCreationForm):
	
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control glass', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control glass', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control glass', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control glass'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small class="text-white">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control glass'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li><small class="text-white">Your password can\'t be too similar to your other personal information.</small></li><li><small class="text-white">Your password must contain at least 8 characters.</small></li><li><small class="text-white">Your password can\'t be a commonly used password.</small></li><li><small class="text-white">Your password can\'t be entirely numeric.</small></li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control glass'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small class="text-white">Enter the same password as before, for verification.</small></span>'	

class ProfileForm(ModelForm):

	phone = forms.CharField(label="", min_length=10, max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), help_text='<span class="form-text text-muted"><small>Phone number should be 10 digit.</small></span>')
	address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
	city = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
	state = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
	zipcode = forms.CharField(label="", max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}))

	class Meta:
		model = Profile
		fields = ["phone", "address", "city", "state", "zipcode"]

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		if not phone.isdigit():
			raise forms.ValidationError("Phone number must be only digits.")
		if len(phone) != 10:
			raise forms.ValidationError("Phone number must be 10 digits.")
		return phone
	
	def clean_zipcode(self):
		zipcode = self.cleaned_data['zipcode']
		if not zipcode.isdigit():
			raise forms.ValidationError("Zipcode must contain only digits.")
		return zipcode
	

class TokenTransactionForm(ModelForm):

	amount = forms.CharField(label="", min_length=3, max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Amount'}), help_text='<span class="form-text text-muted"><small>Amount must be number and positive.</small></span>')

	class Meta:
		model = TokenTransaction
		fields = ['amount']

	def __init__(self, *args, **kwargs):
		super(TokenTransactionForm, self).__init__(*args, **kwargs)

	def clean_amount(self):
		amount = self.cleaned_data['amount']
		if not amount.isdigit():
			raise forms.ValidationError("Amount must contain only digits.")
		int_amount = int(amount)
		if int_amount <= 0:
			raise forms.ValidationError("Amount must be greater than zero.")

		return amount