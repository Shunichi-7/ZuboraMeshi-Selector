from django.shortcuts import render, redirect, get_object_or_404 # render → HTMLを表示、redirect → 別画面へ移動、get_object_or_404 → データベースからデータを探して取得する（なければ404エラー）

from django.contrib.auth.decorators import login_required # ログインしているユーザーだけ実行できるようにする

from .models import Recipe, Favorite # レシピとお気に入り情報を使用する

# Create your views here.

def portfolio(request):
    return redirect("login")

def home(request):
    return render(request, "main/home.html") #レシピ検索やレシピ投稿などの画面を表示できるようにするため、home.htmlを読み込み、ホーム画面を表示する。

def recipe_list(request):

    recipes = Recipe.objects.all()

    cooking_time = request.GET.get("cooking_time")

    if cooking_time:

        recipes = recipes.filter(
            cooking_time__lte=cooking_time
        )
        
    ingredient_count = request.GET.get("ingredient_count")

    if ingredient_count:
        recipes = recipes.filter(
            ingredient_count__lte=ingredient_count
        )
        
    price = request.GET.get("price")

    if price:
        recipes = recipes.filter(
            price__lte=price
        )
        
    mood_tags = request.GET.getlist("mood")

    if mood_tags:
        for mood in mood_tags:
            recipes = recipes.filter(
                mood_tag__contains=mood
            )
            
    zubora_tags = request.GET.getlist("zubora")

    if zubora_tags:
        for zubora in zubora_tags:
            recipes = recipes.filter(
                zubora_tag__contains=zubora
            )
            
    # 検索結果画面に表示するため、
    # ユーザーが選択した検索条件をまとめる
    selected_conditions = []

    if cooking_time:
        selected_conditions.append(f"{cooking_time}分以内")

    if ingredient_count:
        selected_conditions.append(f"材料{ingredient_count}つ以内")

    if price:
        selected_conditions.append(f"{price}円以下")

    for mood in mood_tags:
        selected_conditions.append(mood)

    for zubora in zubora_tags:
        selected_conditions.append(zubora)

    return render(
        request,
        "main/recipe_list.html",
        {
            "recipes": recipes,
            
            # 選択された検索条件を検索結果画面へ渡す
            "selected_conditions": selected_conditions,
        }
    )
    
def recipe_detail(request, recipe_id):
    
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    ) # URLから受け取ったIDと一致するレシピを取得する #レシピが存在しない場合は404エラーを表示する
    
    is_favorite = False # 最初は「お気に入り未登録」として設定する
    
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists() # ユーザーがログインしている場合だけ、お気に入り登録済みか確認する
    
    return render(
        request,
        "main/recipe_detail.html",
        {
            "recipe": recipe,
            "is_favorite": is_favorite,
        },
    )
    
@login_required #ログインしている人だけがレシピ投稿できるようにする。非ログインならログイン画面へ。
def recipe_create(request):
    # 投稿ボタンが押された時の処理
    if request.method == "POST":

        # 入力された料理名を取得する
        title = request.POST.get("title")

        # 入力された調理時間を取得する
        cooking_time = request.POST.get("cooking_time")

        # 入力された金額を取得する
        price = request.POST.get("price")
        
        # 入力された何食分かを取得する
        servings = request.POST.get("servings")
        
        # アップロードされた画像を取得する
        image = request.FILES.get("image")
        
        # 入力された材料をすべて取得する
        ingredient_names = request.POST.getlist("ingredient_name")
        ingredient_amounts = request.POST.getlist("ingredient_amount")
        ingredient_list = []

        for name, amount in zip(ingredient_names, ingredient_amounts):
            ingredient_list.append({
                "name": name,
                "amount": amount,
            })
        # 入力された材料名の数を数える（空欄は除く）
        ingredient_count = len(
            [name for name in ingredient_names if name.strip()]
        )
        # 入力された作り方をすべて取得する
        step_list = request.POST.getlist("steps")
        # 入力されたメモを取得する
        memo = request.POST.get("memo")
        # 選択された気分タグをすべて取得する
        mood_tags = request.POST.getlist("mood_tag")
        # 気分タグをカンマ区切りの文字列に変換する
        mood_tag = ",".join(mood_tags)
        # 選択されたズボラ条件をすべて取得する
        zubora_tags = request.POST.getlist("zubora_tag")
        # ズボラ条件をカンマ区切りの文字列に変換する
        zubora_tag = ",".join(zubora_tags)
        
        # 調理時間・金額・何食分が正しい数字か確認する
        if (
            cooking_time and not cooking_time.isdigit()
            or price and not price.isdigit()
            or servings and not servings.isdigit()
        ):
            return render(
                request,
                "main/recipe_create.html",
                {
                    "error": "※正しい数値を入力してください",
                    "title": title,
                    "cooking_time": cooking_time,
                    "price": price,
                    "servings": servings,
                    "ingredient_list": ingredient_list,
                    "step_list": step_list,
                    "memo": memo,
                    "mood_tags": mood_tags,
                    "zubora_tags": zubora_tags,
                }
            )
        
        # 必須項目が入力されているかチェックする
        if (
            not title
            or not cooking_time
            or not price
            or not servings
            or not any(name.strip() for name in ingredient_names)
            or not any(step.strip() for step in step_list)
            
        ):
            return render(
                request,
                "main/recipe_create.html",
                {
                    "error": "※必須項目を入力してください",
                    "title": title,
                    "cooking_time": cooking_time,
                    "price": price,
                    "servings": servings,
                    "ingredient_list": ingredient_list,
                    "step_list": step_list,
                    "memo": memo,
                    "mood_tags": mood_tags,
                    "zubora_tags": zubora_tags,
                }
            )

        # 材料名と分量を1つの文字列にまとめる
        ingredients = ""

        for name, amount in zip(ingredient_names, ingredient_amounts):

            # 空欄の行は保存しない
            if name or amount:
                ingredients += f"{name}：{amount}\n"
                
        # 作り方を1つの文字列にまとめる
        steps = ""

        for i, step in enumerate(step_list, start=1):

            # 空欄は保存しない
            if step:
                steps += f"{i}. {step}\n"

        # レシピをデータベースに保存する
        Recipe.objects.create(

            title=title,

            cooking_time=cooking_time,

            price=price,
            
            servings=servings,
            
            image=image,
            
            ingredients=ingredients,
            
            steps=steps,
            
            memo=memo,
            
            mood_tag=mood_tag,
            
            zubora_tag=zubora_tag,
            
            user=request.user,
            
            ingredient_count=ingredient_count,

        )
        
        return redirect("recipe_list") # 保存が完了したら、レシピ一覧画面へ移動する

    # レシピ投稿画面を表示する
    return render(
        request,
        "main/recipe_create.html"
    )
    
@login_required
def favorite_toggle(request, recipe_id): # お気に入りの登録・解除を切り替える

    # URLから受け取ったIDと一致するレシピを取得する
    # レシピが存在しない場合は404エラーを表示する
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    # ログイン中のユーザーがお気に入り登録済みか確認する
    favorite = Favorite.objects.filter(
        user=request.user,
        recipe=recipe
    ).first()

    # お気に入り登録済みなら削除する
    if favorite:
        favorite.delete()

    # 未登録なら新しく登録する
    else:
        Favorite.objects.create(
            user=request.user,
            recipe=recipe
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required  
def mypage(request):
    return render(request, "main/mypage.html")

@login_required
def my_recipes(request):

    recipes = Recipe.objects.filter(
        user=request.user
    )

    return render(
        request,
        "main/my_recipes.html",
        {
            "recipes": recipes,
        },
    )

@login_required
def my_recipe_edit(request, recipe_id):

    # 編集するレシピを取得
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user
    )

    # 保存ボタンが押された時
    if request.method == "POST":

        # 入力された料理名を取得
        recipe.title = request.POST.get("title")
        recipe.cooking_time = request.POST.get("cooking_time")
        recipe.price = request.POST.get("price")
        recipe.memo = request.POST.get("memo")
        
        # 入力された何食分かを取得する
        servings = request.POST.get("servings")
        recipe.servings = servings
        
        # 入力された材料をすべて取得する
        ingredient_names = request.POST.getlist("ingredient_name")
        ingredient_amounts = request.POST.getlist("ingredient_amount")
        
        # エラー後も入力した材料を表示するためにまとめる
        ingredient_list = []

        for name, amount in zip(ingredient_names, ingredient_amounts):
            ingredient_list.append({
                "name": name,
                "amount": amount,
            })
            
        # 入力された材料名の数を数える（空欄は除く）
        ingredient_count = len(
            [name for name in ingredient_names if name.strip()]
        )
        
        # 入力された作り方をすべて取得する
        step_list = request.POST.getlist("steps")
        
        # 選択された気分タグをすべて取得する
        mood_tags = request.POST.getlist("mood_tag")

        # 選択されたズボラ条件をすべて取得する
        zubora_tags = request.POST.getlist("zubora_tag")
        
        # 調理時間・金額・何食分が正しい数字か確認する
        if (
            recipe.cooking_time and not str(recipe.cooking_time).isdigit()
            or recipe.price and not str(recipe.price).isdigit()
            or servings and not servings.isdigit()
        ):
            return render(
                request,
                "main/recipe_create.html",
                {
                    "recipe": recipe,
                    "error": "※正しい数値を入力してください",
                    "title": recipe.title,
                    "cooking_time": recipe.cooking_time,
                    "price": recipe.price,
                    "servings": servings,
                    "ingredient_list": ingredient_list,
                    "step_list": step_list,
                    "memo": recipe.memo,
                    "mood_tags": mood_tags,
                    "zubora_tags": zubora_tags,
                }
            )
        
        # 必須項目が入力されているかチェックする
        if (
            not recipe.title
            or not recipe.cooking_time
            or not recipe.price
            or not servings
            or not any(name.strip() for name in ingredient_names)
            or not any(step.strip() for step in step_list)
        ):
            return render(
                request,
                "main/recipe_create.html",
                {
                    "recipe": recipe,
                    "error": "※必須項目を入力してください",
                    "title": recipe.title,
                    "cooking_time": recipe.cooking_time,
                    "price": recipe.price,
                    "servings": servings,
                    "ingredient_list": ingredient_list,
                    "step_list": step_list,
                    "memo": recipe.memo,
                    "mood_tags": mood_tags,
                    "zubora_tags": zubora_tags,
                }
            )

        # 材料名と分量を1つの文字列にまとめる
        ingredients = ""

        for name, amount in zip(ingredient_names, ingredient_amounts):

            # 空欄の行は保存しない
            if name or amount:
                ingredients += f"{name}：{amount}\n"

        recipe.ingredients = ingredients

        # 作り方を1つの文字列にまとめる
        steps = ""

        for i, step in enumerate(step_list, start=1):

            # 空欄は保存しない
            if step:
                steps += f"{i}. {step}\n"

        recipe.steps = steps
        
        # 気分タグを保存する
        recipe.mood_tag = ",".join(mood_tags)

        # ズボラ条件を保存する
        recipe.zubora_tag = ",".join(zubora_tags)
        
        if request.FILES.get("image"):
            recipe.image = request.FILES.get("image")
            
        # 材料数を更新する
        recipe.ingredient_count = ingredient_count

        # データベースを更新
        recipe.save()

        # 詳細画面へ戻る
        return redirect(
            "my_recipe_detail",
            recipe_id=recipe.id
        )
        
    # 編集画面の作り方入力欄に表示するため、保存されている作り方を1つずつリストにまとめる
    step_list = []

    if recipe.steps:
        for step in recipe.steps.splitlines():

            # 「1. 」「2. 」などの番号を取り除く
            if ". " in step:
                step = step.split(". ", 1)[1]

            step_list.append(step)
        
    ingredient_list = []

    if recipe.ingredients:
        for ingredient in recipe.ingredients.splitlines():

            if "：" in ingredient:
                name, amount = ingredient.split("：", 1)

                ingredient_list.append({
                    "name": name,
                    "amount": amount,
                })
            
    return render(
        request,
        "main/recipe_create.html",
        {
            "recipe": recipe,
            "ingredient_list": ingredient_list,
            "step_list": step_list,
            "mood_tags": recipe.mood_tag.split(",") if recipe.mood_tag else [],
            "zubora_tags": recipe.zubora_tag.split(",") if recipe.zubora_tag else [],
        },
    )

@login_required
def favorite_list(request):

    print("ログイン中のユーザー:", request.user)

    favorites = Favorite.objects.filter(
        user=request.user
    )

    print("お気に入り件数:", favorites.count())

    return render(
        request,
        "main/favorite_list.html",
        {
            "favorites": favorites,
        },
    )
    
@login_required
def favorite_detail(request, recipe_id):

    # ログイン中のユーザーがお気に入り登録しているデータを取得する
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    is_favorite = Favorite.objects.filter(
        user=request.user,
        recipe=recipe
    ).exists()

    return render(
        request,
        "main/favorite_detail.html",
        {
            "recipe": recipe,
            "is_favorite": is_favorite,
        },
    )

@login_required
def my_recipe_delete(request, recipe_id):

    # 削除するレシピを取得
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user
    )

    # POSTなら削除する
    if request.method == "POST":

        recipe.delete()

        return redirect("my_recipes")

    # POST以外なら詳細画面へ戻す
    return redirect(
        "my_recipe_detail",
        recipe_id=recipe.id
    )
    
@login_required
def my_recipe_detail(request, recipe_id):

    # ログインしているユーザー本人が投稿したレシピだけ取得する
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        user=request.user
    )

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()

    return render(
        request,
        "main/my_recipe_detail.html",
        {
            "recipe": recipe,
            "is_favorite": is_favorite,
        },
    )