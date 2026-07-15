from django import forms #ユーザー名やメールアドレス、パスワードなどの入力フォームを作成し、入力内容を確認できるようにするため、Djangoに用意されているフォーム機能を読み込む
from django.contrib.auth.forms import UserCreationForm  #ユーザー名とパスワードの入力確認や、パスワードが正しく入力されているかの確認機能を利用するため、Djangoに用意されているユーザー登録用フォームを読み込む
from django.contrib.auth.models import User #アカウント登録フォームで入力されたユーザー名やメールアドレスなどを保存できるようにするため、Djangoに用意されているユーザー情報を管理する機能を読み込む
class SignUpForm(UserCreationForm): # Djangoのユーザー登録フォームをもとに、ズボラ飯セレクター用のアカウント登録フォームを作る
    email = forms.EmailField(
        label="メールアドレス",
        required=True
    )  # メールアドレスの入力欄を作り、入力を必須にする
    
    username = forms.CharField(
        label="ユーザー名"
    )

    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="パスワード再入力",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2") #ユーザー名・メールアドレス・パスワードを新しいユーザー情報として登録できるようにするため、アカウント登録フォームで使用するユーザー情報の保存先とフォームに表示する入力項目を設定する
        