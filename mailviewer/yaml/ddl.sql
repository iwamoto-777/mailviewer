-- Project Name : MailPrev
-- Date/Time    : 2025/07/11 12:04:20
-- Author       : 201001
-- RDBMS Type   : PostgreSQL
-- Application  : A5:SQL Mk-2

/*
  << 注意！！ >>
  BackupToTempTable, RestoreFromTempTable疑似命令が付加されています。
  これにより、drop table, create table 後もデータが残ります。
  この機能は一時的に $$TableName のような一時テーブルを作成します。
  この機能は A5:SQL Mk-2でのみ有効であることに注意してください。
*/

-- 添付ファイル
-- * BackupToTempTable
drop table if exists attach cascade;

-- * RestoreFromTempTable
create table attach (
  attach_id serial not null
  , email_id integer not null
  , attach_name text not null
  , attach_file bytea
  , insert_date date
  , update_date date
  , constraint attach_PKC primary key (attach_id)
) ;

-- メール
-- * BackupToTempTable
drop table if exists mail cascade;

-- * RestoreFromTempTable
create table mail (
  email_id serial not null
  , subject text
  , sender text not null
  , recipients text not null
  , cc text not null
  , sent_at date not null
  , body text not null
  , eml bytea
  , insert_date date
  , update_date date
  , constraint mail_PKC primary key (email_id)
) ;

alter table attach
  add constraint attach_FK1 foreign key (email_id) references mail(email_id);

comment on table attach is '添付ファイル:attach_fileにメールの添付ファイルを格納';
comment on column attach.attach_id is '添付ファイルID';
comment on column attach.email_id is 'メールID';
comment on column attach.attach_name is '添付ファイル名';
comment on column attach.attach_file is '添付ファイル:メールの添付ファイルを格納できる項目にする';
comment on column attach.insert_date is '作成日';
comment on column attach.update_date is '更新日';

comment on table mail is 'メール';
comment on column mail.email_id is 'メールID';
comment on column mail.subject is 'タイトル';
comment on column mail.sender is 'FROM';
comment on column mail.recipients is 'TO';
comment on column mail.cc is 'CC';
comment on column mail.sent_at is '受信日';
comment on column mail.body is '本文';
comment on column mail.eml is 'emlファイル:メールファイルを格納できる項目にする';
comment on column mail.insert_date is '登録日';
comment on column mail.update_date is '更新日';

