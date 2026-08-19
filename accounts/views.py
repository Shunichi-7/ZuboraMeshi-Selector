from django.shortcuts import render, redirect #HTMLファイルを読み込み、ブラウザに画面として表示するため、Djangoのrender機能を読み込む

from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, AccountEditForm  #アカウント作成画面で入力内容を確認し、新しいユーザーを登録できるようにするため、同じaccountsフォルダのforms.pyから、作成したアカウント登録フォームを読み込む

from django.contrib.auth import authenticate, login, logout #ユーザーがログイン・ログアウトを切り替えられるようにするため、ログイン情報の確認、ログイン処理、ログアウト処理を使えるようにする

from django.contrib.auth.models import User  # メールアドレスから登録済みユーザーを探す

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
            user = form.save()   # ユーザーを保存して受け取る
            login(request, user) # 登録したユーザーをそのままログイン状態にする
            return redirect("home") # ホーム画面へ移動

    else:
        form = SignUpForm() #アカウント登録画面を最初に開いた場合は、何も入力されていない登録フォームを作る

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    ) # 登録フォームをsignup.htmlへ渡し、アカウント登録画面に表示する
    
def logout_view(request):
    logout(request) #今のユーザーのログイン状態を解除する
    return redirect("home") #ログアウト後にホーム画面へ移動する

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
            form.save()
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