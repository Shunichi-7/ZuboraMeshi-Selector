from django.shortcuts import render, redirect #HTMLファイルを読み込み、ブラウザに画面として表示するため、Djangoのrender機能を読み込む

from .forms import SignUpForm #アカウント作成画面で入力内容を確認し、新しいユーザーを登録できるようにするため、同じaccountsフォルダのforms.pyから、作成したアカウント登録フォームを読み込む

def login_view(request):
    return render(request, "accounts/login.html") #ログイン画面へアクセスしたときに、login.htmlを読み込んでブラウザに表示する

def signup_view(request): #ユーザーが入力した情報をもとに、実際に新しいアカウントを作成できるようにするため、アカウント登録画面を表示し、登録ボタンが押されたときは入力内容を確認してユーザーを登録する

    if request.method == "POST":
        form = SignUpForm(request.POST) #登録ボタンが押された場合、入力された情報を使って登録フォームを作る

        if form.is_valid():
            form.save() # 入力内容に問題がなければ、新しいユーザーとしてデータベースに保存する
            return redirect("login")

    else:
        form = SignUpForm() #アカウント登録画面を最初に開いた場合は、何も入力されていない登録フォームを作る

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    ) # 登録フォームをsignup.htmlへ渡し、アカウント登録画面に表示する