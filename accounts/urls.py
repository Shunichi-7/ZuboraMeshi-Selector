from django.urls import path #URLを設定するため、Djangoのpath機能を読み込む
from . import views #フォルダにある画面表示の処理を使うため、views.pyを読み込む
from django.contrib.auth import views as auth_views # ログインやパスワード変更など、Djangoに用意されている認証機能を使えるようにする
from .forms import CustomPasswordChangeForm, CustomSetPasswordForm # forms.pyで作成した独自のパスワード変更フォームを使えるようにする

urlpatterns = [
    path("login/", views.login_view, name="login"), #login/へのアクセス時にlogin_viewを実行し、ログイン画面を表示できるようにする
    path("signup/", views.signup_view, name="signup"), # signup/へのアクセス時にsignup_viewを実行し、アカウント作成画面を表示できるようにする
    path("logout/", views.logout_view, name="logout"),
    path("edit-account/", views.account_edit, name="edit_account"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html", # パスワード変更画面として表示するHTMLを指定する
            form_class=CustomPasswordChangeForm, # forms.pyで作成したパスワード変更フォームを使用する。現在と同じパスワードが入力された場合もエラーにする。
            success_url="/mypage/"
        ),
        name="password_change",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.txt",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url="/accounts/login/",
        ),
        name="password_reset",
        ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            form_class=CustomSetPasswordForm,
            success_url="/accounts/login/",
        ),
        name="password_reset_confirm",
    ),
]