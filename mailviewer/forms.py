from django import forms
from django.forms import widgets
from .models import Mail, Attach


class MailSearchForm(forms.Form):
    """
    メール検索フォーム
    """
    subject = forms.CharField(
        label='タイトル',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'タイトルを入力'
        })
    )
    
    sender = forms.CharField(
        label='FROM',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '送信者を入力'
        })
    )
    
    recipients = forms.CharField(
        label='TO',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '宛先を入力'
        })
    )
    
    cc = forms.CharField(
        label='CC',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CCを入力'
        })
    )
    
    sent_at_from = forms.DateField(
        label='受信日（開始）',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    sent_at_to = forms.DateField(
        label='受信日（終了）',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class MailForm(forms.ModelForm):
    """
    メール本文を表示するフォーム（全項目は変更不可）
    """
    class Meta:
        model = Mail
        fields = [
            'email_id', 'subject', 'sender', 'recipients', 
            'cc', 'sent_at', 'body'
        ]
        labels = {
            'email_id': 'メールID',
            'subject': 'タイトル',
            'sender': 'FROM',
            'recipients': 'TO',
            'cc': 'CC',
            'sent_at': '受信日',
            'body': '本文',
        }
        widgets = {
            'email_id': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'sender': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'recipients': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'cc': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'sent_at': forms.DateInput(attrs={'readonly': True, 'class': 'form-control'}),
            'body': forms.Textarea(attrs={'readonly': True, 'class': 'form-control', 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 全フィールドを読み取り専用に設定
        for field in self.fields.values():
            field.disabled = True


class AttachForm(forms.ModelForm):
    """
    添付ファイルを表示するフォーム（全項目は変更不可）
    """
    class Meta:
        model = Attach
        fields = [
            'attach_id', 'email', 'attach_name', 'attach_file'
        ]
        labels = {
            'attach_id': '添付ファイルID',
            'email': 'メールID',
            'attach_name': 'ファイル名',
            'attach_file': '添付ファイル',
        }
        widgets = {
            'attach_id': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'attach_name': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'attach_file': forms.FileInput(attrs={
                'readonly': True, 
                'class': 'form-control',
                'download': 'true'  # ダウンロード可
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 全フィールドを読み取り専用に設定
        for field in self.fields.values():
            field.disabled = True


class EmlUploadForm(forms.Form):
    """
    emlファイルアップロードフォーム
    """
    eml_file = forms.FileField(
        label='EMLファイル',
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.eml'
        })
    )
