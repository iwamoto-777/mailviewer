# MailViewerプロジェクト

MailViewerは、DjangoとPostgreSQLを利用したメール閲覧・管理システムです。

## 概要
- emlファイルのアップロード・解析
- メール一覧・検索・詳細表示
- 添付ファイルの保存・ダウンロード（日本語ファイル名対応）
- シンプルなUIと日本語対応

## ディレクトリ構成
- hello_world/ : Djangoプロジェクト本体
- mailviewer/  : メール管理アプリケーション
    - models.py, views.py, forms.py, templates/, static/, migrations/
- menv/       : Python仮想環境
- requirements.txt : 必要パッケージ
- manage.py   : Django管理コマンド

## 主な機能
- emlファイル取込画面でメールデータと添付ファイルを一括保存
- メール一覧画面で検索・絞り込み
- メール詳細画面で本文・添付ファイル表示

## 実行方法
1. 仮想環境の有効化
2. 必要パッケージのインストール
   ```
   pip install -r requirements.txt
   ```
3. マイグレーション実行
   ```
   python manage.py migrate
   ```
4. サーバ起動
   ```
   python manage.py runserver
   ```

## ライセンス
MIT License

## VerUP予定
- デザインの改善
    - 検索条件の並びをスリム化
    - メール一覧はスマートな行のデザインに改善
- メールファイルをディレクトリ構造で保存
    - フォルダ形式のUIを追加
    - フォルダの作成・変更・削除は右クリックで操作
    - 取り込んだファイルは、取込用フォルダへ格納
    - ファイル、フォルダはドラッグ＆ドロップで移動