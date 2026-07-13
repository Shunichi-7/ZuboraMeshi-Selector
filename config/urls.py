"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin #Djangoの管理画面を使用できるようにするため、管理画面機能を読み込む
from django.urls import path, include #URLを設定するpathと、各アプリのURL設定を読み込むincludeを使用するため、DjangoのURL機能を読み込む

urlpatterns = [
    path('admin/', admin.site.urls), #URLの末尾がadmin/だったら、Djangoの管理画面へ案内する
    path("", include("main.urls")), #ポートフォリオ画面やホーム画面を表示できるようにするため、プロジェクト全体のURL設定とmain/urls.pyをつないだ
    path("accounts/", include("accounts.urls")), #ログイン画面やアカウント作成画面へアクセスできるようにするため、プロジェクト全体のURL設定とaccounts/urls.pyをつないだ
]
