from django.urls import path
from . import views
from .views import UserEnrolledListCreateView,UserEnrolledRetrieveUpdateDestroyView,get_data,create_data,UpdateData,TaskDeleteView,AssetDetailView,AssetUpdateView,AssetDeleteView,DownloadDatabaseView,ActionStatusAPIView,ChangeDetectionView,LoginAPIView,AssetCreateAPIView,AssetListAPIView,UserEnrollListCreateAPIView,UserEnrollDetailAPIView,SiteListAPIView,SiteUpdateView,SiteDeleteView,CompanyUpdateView,CompanyDeleteView,NotificationList
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.login_view,name='login'),
    #path('login1/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("check/", views.check_data, name="check"),
    path('api_user_enro/', UserEnrolledListCreateView.as_view(), name='user_enro1'),
    path('api_user_enro/<int:pk>/', UserEnrolledRetrieveUpdateDestroyView.as_view(), name='user_enro2'),
    path('get_all/',get_data.as_view(),name='get_all'),
    path('create/',create_data.as_view(),name='create'),
    path('notification/',views.post_notification, name='notification'),
    path('upload/', views.upload_file, name='upload'),
    path('orientation/', views.orientation_task, name='orientation'),
    path('report/', views.report_view, name='report'),
    path('update/<int:pk>/', UpdateData.as_view(), name='user_update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('app2_login/',views.login_view,name='app2_login'),
    path('sites/',views.site_view,name='sites'),
    path('app2logout/',views.app2_logout,name='app2logout'),
    path('management/',views.management_view,name='management'),
    path('worker_edit/',views.edit_worker,name='worker_edit'),
    path('asset_manage/',views.asset_management,name='asset_manage'),
    path('asset_site/',views.asset_site,name='asset_site'),
    path('add_asset/',views.add_asset,name='add_asset'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='asset_detail'),
    path('edit_asset/<int:pk>/', AssetUpdateView.as_view(), name='asset_edit'),
    path('delete_asset/<int:pk>/', AssetDeleteView.as_view(), name='asset_delete'),
    path('download-db/', DownloadDatabaseView.as_view(), name='download-db'),  # download in sqlite3 that is binary
    path('detect_changes/', ChangeDetectionView.as_view(), name='detect-changes'),
    path('exit/',views.exit,name='exit'),
    path('setting_t/',views.setting_turn,name='setting_t'),
    path('action_status/', ActionStatusAPIView.as_view(), name='action_status'),
    path('login_api/', LoginAPIView.as_view(), name='api-login'),
    path('users/', UserEnrollListCreateAPIView.as_view(), name='user-enroll-list-create'),
    path('users/<int:tag_id>/', UserEnrollDetailAPIView.as_view(), name='user-enroll-detail'), 
    path('get_assets_api/', AssetListAPIView.as_view(), name='asset-list'),
    path('asset_api/', AssetCreateAPIView.as_view(), name='asset-create'),
    path('exits/', views.ExitListCreateAPIView.as_view(), name='exit-list-create'),
    path('exits/<int:asset_id>/', views.ExitDetailAPIView.as_view(), name='exit-detail'),
    path('sites_api/', SiteListAPIView.as_view(), name='site-list'),
    path('add_site/', views.add_site, name='add_site'),
    path('edit_site/<int:pk>/', SiteUpdateView.as_view(), name='edit_sites'),
    path('delete_site/<int:pk>/', SiteDeleteView.as_view(), name='delete_sites'),
    path('company/', views.company_view, name='company'),
    path('add_company/', views.add_company_data, name='add_company'),
    path('edit_company/<int:pk>/', CompanyUpdateView.as_view(), name='edit_company'),
    path('delete_company/<int:pk>/', CompanyDeleteView.as_view(), name='delete_company'),
    path('time/', views.timesche, name='time'),
    path('notification_api/', NotificationList.as_view(), name='notification-list'),
    path('success/', views.success_page, name='success'),
   


] 




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)