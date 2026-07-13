from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, "accounts/login.html") # ログイン画面を表示する処理

def signup_view(request):
    return render(request, "accounts/signup.html") # アカウント作成画面を表示する処理
