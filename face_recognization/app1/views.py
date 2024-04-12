from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,NotificationForm,upload_form,YourModelForm,AssetForm,SiteForm,CompanyForm,timescheduleForm
from .models import CustomUser,UserEnrolled,Asset,Exit,Site,company,timeschedule,Notification,Upload_File
from .serializers import LoginSerializer,AssetSerializer,UserEnrolledSerializer,ExitSerializer,SiteSerializer,ActionStatusSerializer,NotificationSerializer,UploadedFileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import UserEnrolledSerializer
from django.views.generic.list import ListView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic import UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse,HttpResponse
from django.db import connection
from rest_framework.views import APIView
from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .middleware import ActionStatusMiddleware
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser

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

def post_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            return redirect('success')
    else:
        form = NotificationForm()
    return render(request, 'app1/notification.html', {'form': form})

def success_page(request):
    return render(request, 'app1/success.html')

def upload_file(request):
    if request.method == 'POST':
        form = upload_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'file saved successfully'})
    else:
        form = upload_form()
    return render(request, 'app1/upload.html', {'form': form})


def report_view(request):
    return render(request, 'app1/report.html')


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
            try:
                form.save()
                return redirect('asset_site')
            except ValidationError as e:
                form.add_error('asset_id', str(e))
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
    assets = Exit.objects.all()
    return render(request, 'app1/exit_status.html', {'assets': assets})

def site_view(request):
    sites = Site.objects.all()
    total_users = UserEnrolled.objects.count()
    active_users = UserEnrolled.objects.filter(status='active').count()
    inactive_users = UserEnrolled.objects.filter(status='inactive').count()
    print(f"Total Users: {total_users}, Active Users: {active_users}, Inactive Users: {inactive_users}")
    return render(request, 'app1/site.html', {
        'sites': sites,
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
    })


def time_shedule(request):
    return render(request,'app1/time_shedule.html')

def setting_turn(request):
    return render(request,'app1/setting_turn.html')


class ActionStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        status_data = {'status': 1 if ActionStatusMiddleware.perform_action() else 0}
        serializer = ActionStatusSerializer(status_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeDetectionView(APIView):
    def get(self, request, *args, **kwargs):
       
        has_changes = cache.get('has_changes', False)
        
        if has_changes:
            
            cache.set('has_changes', False)
            return Response({'changes_detected': 1})
        else:
            return Response({'changes_detected': 0})

@receiver(post_save, sender=UserEnrolled)
def book_change_handler(sender, instance, **kwargs):
 
    cache.set('has_changes', True)

@receiver(pre_delete, sender=UserEnrolled)
def book_delete_handler(sender, instance, **kwargs):
   
    cache.set('has_changes', True)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
           
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AssetCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetListAPIView(generics.ListAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class UserEnrollListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserEnrolled.objects.all()
    serializer_class = UserEnrolledSerializer

    def perform_create(self, serializer):
        serializer.save(orientation=self.request.data.get('orientation'))


class UserEnrollDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserEnrolled.objects.all()
    serializer_class = UserEnrolledSerializer

    def get_object(self):
        queryset = self.get_queryset()
        tag_id = self.kwargs.get('tag_id')  
        obj = generics.get_object_or_404(queryset, tag_id=tag_id) 
        return obj


class ExitListCreateAPIView(generics.ListCreateAPIView):
    queryset = Exit.objects.all()
    serializer_class = ExitSerializer


class ExitDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exit.objects.all()
    serializer_class = ExitSerializer
    def get_object(self):
        queryset = self.get_queryset()
        asset_id = self.kwargs.get('asset_id')
        obj = generics.get_object_or_404(queryset, asset_id=asset_id)
        return obj


class SiteListAPIView(generics.ListAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

def add_site(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sites') 
    else:
        form = SiteForm()
    return render(request, 'app1/add_site.html', {'form': form})

class SiteUpdateView(UpdateView):
    model = Site
    form_class = SiteForm
    template_name = 'app1/add_site.html'
    success_url = '/sites/'

    def get(self, request, *args, **kwargs):
        
        asset_instance = get_object_or_404(Site, pk=kwargs['pk'])
        
        form = self.form_class(instance=asset_instance)
        
        return self.render_to_response({'form': form})


class SiteDeleteView(DeleteView):
    model = Site
    template_name = 'app1/data_confirm_delete2.html'
    success_url = reverse_lazy('sites')


def company_view(request):
    compy = company.objects.all() 
    return render(request, 'app1/company.html', {'compy': compy})

def add_company_data(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('company') 
    else:
        form = CompanyForm()
    return render(request, 'app1/add_company.html', {'form': form})


class CompanyUpdateView(UpdateView):
    model = company
    form_class = CompanyForm
    template_name = 'app1/add_company.html'
    success_url = '/company/'

    def get(self, request, *args, **kwargs):
        
        asset_instance = get_object_or_404(company, pk=kwargs['pk'])
        
        form = self.form_class(instance=asset_instance)
        
        return self.render_to_response({'form': form})


class CompanyDeleteView(DeleteView):
    model = company
    template_name = 'app1/data_confirm_delete3.html'
    success_url = reverse_lazy('company')


def timesche(request):
    data = timeschedule.objects.all()
    return render(request, 'app1/time_shedule.html', {'data': data})


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def add_timesh(request):
    if request.method == 'POST':
        form = timescheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('time') 
    else:
        form = timescheduleForm()
    return render(request, 'app1/add_time.html', {'form': form})