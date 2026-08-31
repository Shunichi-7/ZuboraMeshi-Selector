from django.shortcuts import render, redirect #HTMLファイルを読み込み、ブラウザに画面として表示するため、Djangoのrender機能を読み込む

from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST # ログアウト処理を、ボタンから送信された場合だけ実行できるようにする機能を読み込む

from .forms import SignUpForm, AccountEditForm  #アカウント作成画面で入力内容を確認し、新しいユーザーを登録できるようにするため、同じaccountsフォルダのforms.pyから、作成したアカウント登録フォームを読み込む

from django.contrib.auth import authenticate, login, logout #ユーザーがログイン・ログアウトを切り替えられるようにするため、ログイン情報の確認、ログイン処理、ログアウト処理を使えるようにする

from django.contrib.auth.models import User  # メールアドレスから登録済みユーザーを探す

# 登録や変更などの処理が完了したことをユーザーに知らせるメッセージ機能を読み込む
from django.contrib import messages

# パスワード変更やパスワード再設定など、Djangoに用意されている認証機能を使用する
from django.contrib.auth import views as auth_views

def login_view(request):
    # ログイン失敗時に表示するエラーメッセージ
    error_message = ""

    if request.method == "POST":

        # 入力されたメールアドレスとパスワードを取得する
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 入力されたメールアドレスと一致するユーザーを探す
        user_data = User.objects.filter(email=email).first()

        # 入力されたメールアドレスのユーザーが存在しない場合
        if user_data is None:
            error_message = "正しいメールアドレスとパスワードを入力してください。"

        else:
            # メールアドレスから取得したユーザー名と、
            # 入力されたパスワードを使ってログイン情報を確認する
            user = authenticate(
                request,
                username=user_data.username,
                password=password
            )

            # ログイン情報が正しい場合
            if user is not None:

                # ログイン状態にする
                login(request, user)
                
                # ログインが完了したことを画面に表示する
                messages.success(
                    request,
                    "ログインしました。"
                )

                # ホーム画面へ移動する
                return redirect("home")

            # パスワードが間違っている場合
            else:
                error_message = "正しいメールアドレスとパスワードを入力してください。"

    # 最初に開いた場合、またはログインに失敗した場合
    return render(
        request,
        "accounts/login.html",
        {
            "error_message": error_message,
        }
    )

def signup_view(request): #ユーザーが入力した情報をもとに、実際に新しいアカウントを作成できるようにするため、アカウント登録画面を表示し、登録ボタンが押されたときは入力内容を確認してユーザーを登録する

    if request.method == "POST":
        form = SignUpForm(request.POST) #登録ボタンが押された場合、入力された情報を使って登録フォームを作る

        if form.is_valid():

            # 入力されたアカウント情報をデータベースに保存する
            user = form.save()

            # 登録したユーザーをそのままログイン状態にする
            login(request, user)

            # アカウント登録が完了したことを次の画面に表示する
            messages.success(
                request,
                "アカウント登録が完了しました。"
            )

            # ホーム画面へ移動する
            return redirect("home")

    else:
        form = SignUpForm() #アカウント登録画面を最初に開いた場合は、何も入力されていない登録フォームを作る

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    ) # 登録フォームをsignup.htmlへ渡し、アカウント登録画面に表示する
    
# URLを開いただけでログアウトされないように、ボタンからの送信だけを受け付ける
@require_POST
def logout_view(request):

    # 現在のユーザーのログイン状態を解除する
    logout(request)

    # ログアウトが完了したことを次の画面に表示する
    messages.success(
        request,
        "ログアウトしました。"
    )

    # ホーム画面へ移動する
    return redirect("home")

@login_required
def mypage_view(request):
    return render(request, "accounts/mypage.html")

@login_required
def account_edit(request):

    if request.method == "POST":

        form = AccountEditForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            # 変更されたユーザー名とメールアドレスを保存する
            form.save()

            # アカウント情報の変更が完了したことを次の画面に表示する
            messages.success(
                request,
                "アカウント情報を変更しました。"
            )

            # マイページへ移動する
            return redirect("mypage")

    else:

        form = AccountEditForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/account_edit.html",
        {
            "form": form,
        },
    )
    
# Django標準のパスワード変更処理を引き継ぎ、変更完了後にサクセスメッセージを表示できるようにする
class PasswordChangeView(auth_views.PasswordChangeView):

    # 入力内容に問題がなく、パスワード変更が成功した場合に実行する
    def form_valid(self, form):

        # Django標準のパスワード変更処理を実行する
        response = super().form_valid(form)

        # パスワード変更が完了したことを移動先の画面に表示する
        messages.success(
            self.request,
            "パスワードを変更しました。"
        )

        # Django標準のパスワード変更後の処理結果を返す
        return response
    
# Django標準のパスワード再設定メール送信処理を引き継ぎ、メール送信受付後にサクセスメッセージを表示できるようにする
class PasswordResetView(auth_views.PasswordResetView):

    # メールアドレスの入力内容に問題がない場合に実行する
    def form_valid(self, form):

        # Django標準のパスワード再設定メール送信処理を実行する
        response = super().form_valid(form)

        # 再設定メールの送信処理が完了したことを移動先の画面に表示する
        messages.success(
            self.request,
            "パスワード再設定用のメールを送信しました。"
        )

        # Django標準のメール送信後の処理結果を返す
        return response
    
# Django標準の新しいパスワード設定処理を引き継ぎ、再設定完了後にサクセスメッセージを表示できるようにする
class PasswordResetConfirmView(
    auth_views.PasswordResetConfirmView
):

    # 新しいパスワードの入力内容に問題がない場合に実行する
    def form_valid(self, form):

        # Django標準の新しいパスワード保存処理を実行する
        response = super().form_valid(form)

        # パスワードの再設定が完了したことをログイン画面に表示する
        messages.success(
            self.request,
            "パスワードを再設定しました。"
        )

        # Django標準のパスワード再設定後の処理結果を返す
        return response