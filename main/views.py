from django.shortcuts import render

# Create your views here.

def portfolio(request):
    return render(request, "main/portfolio.html")

def home(request):
    return render(request, "main/home.html") #レシピ検索やレシピ投稿などの画面を表示できるようにするため、home.htmlを読み込み、ホーム画面を表示する。

