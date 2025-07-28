from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from .models import Mail, Attach
from .forms import MailSearchForm, EmlUploadForm, MailForm
import email
from email import policy
from email.parser import BytesParser
from datetime import datetime
from pytz import timezone
import mimetypes


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
            eml_file = request.FILES['eml_file']
            try:
                # EMLファイルを解析
                from io import BytesIO
                msg = BytesParser(policy=policy.default).parse(BytesIO(eml_file.read()))

                # sent_atのフォーマットを適用
                sent_at = msg['date']
                if sent_at:
                    sent_at = datetime.strptime(sent_at, '%a, %d %b %Y %H:%M:%S %z')

                # Mailモデルに保存
                mail = Mail.objects.create(
                    subject=msg['subject'],
                    sender=msg['from'],
                    recipients=msg['to'],
                    cc=msg.get('cc', ''),
                    sent_at=sent_at,
                    body=msg.get_body(preferencelist=('plain', 'html')).get_content()
                )

                # 添付ファイルをAttachモデルに保存
                for part in msg.iter_attachments():
                    Attach.objects.create(
                        email=mail,
                        attach_name=part.get_filename(),
                        attach_file=part.get_content()
                    )

                message = 'ファイルが正常にアップロードされ、処理されました。'
            except Exception as e:
                message = f'エラーが発生しました: {str(e)}'

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
    # メールデータを取得
    mail = get_object_or_404(Mail, email_id=mail_id)

    # 添付ファイルを取得
    attachments = Attach.objects.filter(email=mail)

    # メールデータをMailFormにセット
    mailForm = MailForm(instance=mail)

    # コンテキストを設定
    context = {
        'title': f'メール詳細 - {mail.subject}',
        'mailForm': mailForm,
        'attachments': attachments
    }

    return render(request, 'mailviewer/mail_detail.html', context)


def attach(request, attach_id):
    """
    添付ファイルをダウンロードする
    """
    attach = get_object_or_404(Attach, attach_id=attach_id)
    if not attach.attach_file:
        return HttpResponse("ファイルが存在しません。", status=404)

    mime_type, _ = mimetypes.guess_type(attach.attach_name)
    response = HttpResponse(attach.attach_file, content_type=mime_type or 'application/octet-stream')
    # 日本語ファイル名対応（RFC 6266）
    from urllib.parse import quote
    filename = quote(attach.attach_name)
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{filename}"
    return response
