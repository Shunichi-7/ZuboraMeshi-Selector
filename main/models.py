from django.db import models

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    cooking_time = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    ingredient_count = models.PositiveIntegerField(default=1)
    servings = models.PositiveIntegerField(default=1)
    steps = models.TextField(blank=True)
    memo = models.TextField(blank=True)
    zubora_tag = models.CharField(max_length=30, blank=True)
    mood_tag = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to="recipe_images/", blank=True)
    
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    @property
    def zubora_tags(self):
        return [tag.strip() for tag in self.zubora_tag.split(",") if tag.strip()]

    @property
    def mood_tags(self):
        return [tag.strip() for tag in self.mood_tag.split(",") if tag.strip()]
    
    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    ) # お気に入りしたユーザーを保存する

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    ) # お気に入りされたレシピを保存する

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}" # 管理画面で「ユーザー名 - レシピ名」と表示する