from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Upload_data,Asset,Site,company,UserEnrolled,Notification,timeschedule,Turnstile_S,Exit
from django.contrib.auth import get_user_model



CustomUser = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class YourModelForm(forms.ModelForm):
    class Meta:
        model = UserEnrolled
        fields = '__all__'
        widgets = {
            'orientation': forms.ClearableFileInput(attrs={'accept': 'application/pdf, application/msword, image/jpeg, image/jpg'}),
        }
        labels = {
            'orientation': 'Upload Orientation File',
        }
        
    #job_role = forms.ChoiceField(choices=UserEnrolled.job_role, widget=forms.Select(attrs={'class': 'form-control'}))


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['subject', 'description', 'username']


class upload_form(forms.ModelForm):
    class Meta:
        model = Upload_data
        fields = ['uploaded_file']


class AssetForm(forms.ModelForm):
    asset_category_choices = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'), 
    ]
    asset_category = forms.ChoiceField(choices=asset_category_choices)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Asset
        fields = [ 'asset_id','asset_name', 'description', 'asset_category','status']
      

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.upper()


class CompanyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = '__all__'
        widgets = {
            'safety_insurance': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.jpeg,.jpg'}),
        }
        

class timescheduleForm(forms.ModelForm):
    class Meta:
        model = timeschedule
        fields = '__all__'


class TurnstileForm(forms.ModelForm):
    class Meta:
        model = Turnstile_S
        fields = ['turnstile_id','location','safety_confirmation']


class ExitForm(forms.ModelForm):
    class Meta:
        model = Exit
        fields = ['asset_id','asset_name','location']