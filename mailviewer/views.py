from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Mail, Attach
from .forms import MailSearchForm


def index(request):
    """
    メール一覧を表示する
    """
    form = MailSearchForm()
    mails = []
    message = ''
    
    if request.method == 'POST':
        form = MailSearchForm(request.POST)
        if form.is_valid():
            # 検索条件でフィルタリング
            queryset = Mail.objects.all()
            
            # 各フィールドでの検索条件を適用
            if form.cleaned_data['subject']:
                queryset = queryset.filter(subject__icontains=form.cleaned_data['subject'])
            
            if form.cleaned_data['sender']:
                queryset = queryset.filter(sender__icontains=form.cleaned_data['sender'])
            
            if form.cleaned_data['recipients']:
                queryset = queryset.filter(recipients__icontains=form.cleaned_data['recipients'])
            
            if form.cleaned_data['cc']:
                queryset = queryset.filter(cc__icontains=form.cleaned_data['cc'])
            
            if form.cleaned_data['sent_at_from']:
                queryset = queryset.filter(sent_at__gte=form.cleaned_data['sent_at_from'])
            
            if form.cleaned_data['sent_at_to']:
                queryset = queryset.filter(sent_at__lte=form.cleaned_data['sent_at_to'])
            
            mails = queryset.order_by('-sent_at')
            
            if not mails.exists():
                message = 'データがありません。'
    else:
        # GET処理：初期表示
        message = 'データがありません。'
    
    context = {
        'title': 'メール一覧',
        'form': form,
        'message': message,
        'mails': mails
    }
    
    return render(request, 'mailviewer/index.html', context)


def input_view(request):
    """
    emlファイルの取込画面
    """
    form = EmlUploadForm()
    message = ''
    
    if request.method == 'POST':
        form = EmlUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO: emlファイルの解析とデータベース保存処理を実装
            files = request.FILES.getlist('eml_files')
            if files:
                message = f'{len(files)}件のファイルがアップロードされました。'
            else:
                message = 'ファイルが選択されていません。'
    
    context = {
        'title': 'emlファイル取込',
        'form': form,
        'message': message
    }
    
    return render(request, 'mailviewer/input.html', context)


def mail_detail(request, mail_id):
    """
    メール本文の詳細表示
    """
    mail = get_object_or_404(Mail, email_id=mail_id)
    attachments = Attach.objects.filter(email=mail)
    
    context = {
        'title': f'メール詳細 - {mail.subject}',
        'mail': mail,
        'attachments': attachments
    }
    
    return render(request, 'mailviewer/mail_detail.html', context)
