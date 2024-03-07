from django.urls import path
from . import views
from .views import UserEnrolledListCreateView,UserEnrolledRetrieveUpdateDestroyView,get_data,create_data,msg,UpdateData,TaskDeleteView,AssetDetailView,AssetUpdateView,AssetDeleteView,DownloadDatabaseView
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
    path('success/',msg.as_view(),name='success'),
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
    path('exit/',views.exit,name='exit'),
    path('company/',views.get_company,name='company'),
    path('time/',views.time_shedule,name='time'),
    path('setting_t/',views.setting_turn,name='setting_t'),

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)