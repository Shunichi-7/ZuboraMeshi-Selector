from django.urls import path
from . import views


urlpatterns = [
    path("", views.portfolio, name="portfolio"),
    path("home/", views.home, name="home"),
    path("recipes/", views.recipe_list, name="recipe_list"), #レシピ検索結果画面を表示できるようにする。
    path("recipes/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"), #レシピ詳細画面を表示できるようにする。
    path("recipes/<int:recipe_id>/favorite/",views.favorite_toggle,name="favorite_toggle",),  # お気に入り登録・解除を行う
    path("recipes/create/",views.recipe_create,name="recipe_create",),
    path("mypage/", views.mypage, name="mypage"),
    path("my-recipes/", views.my_recipes, name="my_recipes"),
    path("my-recipes/<int:recipe_id>/",views.my_recipe_detail,name="my_recipe_detail",),
    path("my-recipes/<int:recipe_id>/edit/", views.my_recipe_edit, name="my_recipe_edit"),
    path("favorites/", views.favorite_list, name="favorite_list"),
    path("favorites/<int:recipe_id>/", views.favorite_detail, name="favorite_detail"),
    path("my-recipes/<int:recipe_id>/delete/",views.my_recipe_delete,name="my_recipe_delete",),
] 

