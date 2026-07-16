from django.urls import path
from . import views


urlpatterns = [
    path("", views.portfolio, name="portfolio"),
    path("home/", views.home, name="home"),
] #ズボラ飯セレクターのホーム画面をブラウザに表示できるようにするため、「/home/」へアクセスしたときに、views.pyのhomeを呼び出す。
