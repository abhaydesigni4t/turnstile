from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Upload_data
from django.contrib.auth import get_user_model
from .models import UserEnrolled,Notification,Orientation

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

class OrientationForm(forms.ModelForm):
    class Meta:
        model = Orientation
        fields = ['attachments']


from .models import Asset


class AssetForm(forms.ModelForm):
    asset_category_choices = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
       
    ]

    asset_category = forms.ChoiceField(choices=asset_category_choices)

    class Meta:
        model = Asset
        fields = ['asset_name','asset_id','description','asset_category']

   

