from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,NotificationForm,upload_form,OrientationForm,YourModelForm,AssetForm
from .models import CustomUser,UserEnrolled,Asset
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserEnrolledSerializer
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse,HttpResponse
from django.db import connection
from rest_framework.views import APIView
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('sites')
            else:             
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'app1/login.html', {'form': form})


def user_logout(request):
    logout(request)
    form = LoginForm()
    return render(request, 'app1/login.html', {'form': form})

@api_view(['POST'])
def check_data(request):
    username = request.data.get('username')
    password = request.data.get('password') 
    try:
        user = CustomUser.objects.get(username=username)
        if user.check_password(password):      
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        pass
    return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

class UserEnrolledListCreateView(ListCreateAPIView):
    queryset = UserEnrolled.objects.all()
    serializer_class = UserEnrolledSerializer

class UserEnrolledRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = UserEnrolled.objects.all()
    serializer_class = UserEnrolledSerializer

class msg(TemplateView):
    template_name = 'app1/success.html'

def post_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            return JsonResponse({'message': 'Notification saved successfully'})
    else:
        form = NotificationForm()
    return render(request, 'app1/notification.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = upload_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'file saved successfully'})
    else:
        form = upload_form()
    return render(request, 'app1/upload.html', {'form': form})


def orientation_task(request):
    if request.method == 'POST':
        form = OrientationForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'file saved successfully'})
        else:
            print(form.errors)
    else:
        form = OrientationForm()
    return render(request, 'app1/orientation.html', {'form': form})


def report_view(request):
    return render(request, 'app1/report.html')


from django.views.generic import ListView
from .models import UserEnrolled

class get_data(ListView):
    model = UserEnrolled
    template_name = 'app1/getdata.html'
    context_object_name = 'data'
    paginate_by = 5  

    def get_queryset(self):
        return UserEnrolled.objects.all()

class create_data(CreateView):
    model = UserEnrolled 
    form_class = YourModelForm     
    template_name = 'app1/add_user.html'
    success_url = reverse_lazy('get_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = UserEnrolled.objects.all()
        return context

class UpdateData(UpdateView):
    model = UserEnrolled 
    fields = '__all__'     
    template_name = 'app1/add_user.html'
    success_url = reverse_lazy('get_all')

class TaskDeleteView(DeleteView):
    model = UserEnrolled
    template_name = 'app1/data_confirm_delete.html'
    success_url = reverse_lazy('get_all')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('sites')
            else:             
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'app1/app2_login.html', {'form': form})


def app2_logout(request):
    logout(request)
    return redirect('app2_login')

def management_view(request):
    return render(request,'app1/management.html')


def edit_worker(request):
    return render(request,'app1/worker_edit.html')

def asset_management(request):
    return render(request,'app1/asset_management.html')

def asset_site(request):
    assets = Asset.objects.all()
    return render(request,'app1/asset_site.html',{'assets': assets})


def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_site')
    else:
        form = AssetForm()
    return render(request, 'app1/add_asset.html', {'form': form})


class AssetDetailView(DetailView):
    model = Asset
    template_name = 'app1/view_asset.html'  
    context_object_name = 'asset'


class AssetUpdateView(UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'app1/add_asset.html'
    success_url = '/asset_site/'

    def get(self, request, *args, **kwargs):
        
        asset_instance = get_object_or_404(Asset, pk=kwargs['pk'])
        
        form = self.form_class(instance=asset_instance)
        
        return self.render_to_response({'form': form})


class AssetDeleteView(DeleteView):
    model = Asset
    template_name = 'app1/data_confirm_delete1.html'
    success_url = reverse_lazy('asset_site')


class DownloadDatabaseView(APIView):
    def get(self, request, *args, **kwargs):  
        db_path = connection.settings_dict['NAME']
        with open(db_path, 'rb') as db_file:
            response = HttpResponse(db_file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=db.sqlite3'
            return response

def exit(request):
    return render(request,'app1/exit_status.html')


def site_view(request):
    total_users = UserEnrolled.objects.count()
    active_users = UserEnrolled.objects.filter(status='active').count()
    inactive_users = UserEnrolled.objects.filter(status='inactive').count()
    print(f"Total Users: {total_users}, Active Users: {active_users}, Inactive Users: {inactive_users}")
    return render(request, 'app1/site.html', {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
    })


def get_company(request):
    return render(request,'app1/company.html')

def time_shedule(request):
    return render(request,'app1/time_shedule.html')

def setting_turn(request):
    return render(request,'app1/setting_turn.html')