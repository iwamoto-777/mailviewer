from django.urls import path
from . import views

app_name = 'mailviewer'

urlpatterns = [
    # MailViewerシステムのメイン画面
    path('', views.index, name='index'),
    
    # emlファイルの取込画面
    path('input/', views.input_view, name='input'),
    
    # メール本文
    path('mail/<int:mail_id>/', views.mail_detail, name='mail_detail'),

    # 添付ファイルのダウンロード
    path('attach/<int:attach_id>/', views.attach, name='attach'),
]
