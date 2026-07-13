from django.urls import path #URLを設定するため、Djangoのpath機能を読み込む
from . import views #フォルダにある画面表示の処理を使うため、views.pyを読み込む

urlpatterns = [
    path("login/", views.login_view, name="login"), #login/へのアクセス時にlogin_viewを実行し、ログイン画面を表示できるようにする
    path("signup/", views.signup_view, name="signup"), # signup/へのアクセス時にsignup_viewを実行し、アカウント作成画面を表示できるようにする
]