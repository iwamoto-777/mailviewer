from django.db import models
from django.utils import timezone


class Mail(models.Model):
    """
    メールテーブル
    """
    email_id = models.AutoField(primary_key=True, verbose_name='メールID')
    subject = models.TextField(blank=True, null=True, verbose_name='タイトル')
    sender = models.TextField(verbose_name='FROM')
    recipients = models.TextField(verbose_name='TO')
    cc = models.TextField(verbose_name='CC')
    sent_at = models.DateTimeField(verbose_name='受信日')
    body = models.TextField(verbose_name='本文')
    eml = models.BinaryField(blank=True, null=True, verbose_name='emlファイル:メールファイルを格納できる項目にする')
    insert_date = models.DateTimeField(auto_now_add=True, verbose_name='登録日')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新日')

    class Meta:
        db_table = 'mail'
        verbose_name = 'メール'
        verbose_name_plural = 'メール'

    def __str__(self):
        return f"{self.subject} - {self.sender}"


class Attach(models.Model):
    """
    添付ファイルテーブル
    """
    attach_id = models.AutoField(primary_key=True, verbose_name='添付ファイルID')
    email = models.ForeignKey(
        Mail, 
        on_delete=models.CASCADE, 
        db_column='email_id',
        verbose_name='メールID'
    )
    attach_name = models.TextField(verbose_name='添付ファイル名')
    attach_file = models.BinaryField(blank=True, null=True, verbose_name='添付ファイル:メールの添付ファイルを格納できる項目にする')
    insert_date = models.DateTimeField(auto_now_add=True, verbose_name='作成日')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新日')

    class Meta:
        db_table = 'attach'
        verbose_name = '添付ファイル'
        verbose_name_plural = '添付ファイル'

    def __str__(self):
        return f"{self.attach_name} ({self.email.subject})"
