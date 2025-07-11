# 変数
$app_name = "mailviewer"
$venv_name = "menv"

# # menvという名前でvenv仮想環境を作成
# python -m venv $venv_name

# # 仮想環境を有効化
# # Windowsの場合
# .\$venv_name\Scripts\Activate.ps1

# # LinuxやMacの場合
# # source $venv_name/bin/activate

# 必要なパッケージをインストール
pip install -r requirements.txt

# startapp
python manage.py startapp $app_name

# settings.pyにアプリケーションを追加
$settings_path = "mailviewer/settings.py"
$settings_content = Get-Content $settings_path
$settings_content += "`nINSTALLED_APPS += ['$app_name']"
Set-Content $settings_path $settings_content

# .envファイルを作成
$env_content = @"
DATABASE_URL=postgresql://iar:iar@localhost:5434/iar
SECRET_KEY=your_secret_key_here
DEBUG=True  
"@
Set-Content -Path ".env" -Value $env_content

