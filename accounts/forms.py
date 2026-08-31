from django import forms #ユーザー名やメールアドレス、パスワードなどの入力フォームを作成し、入力内容を確認できるようにするため、Djangoに用意されているフォーム機能を読み込む
import re # パスワードに大文字・小文字・数字が含まれているか確認するため、正規表現という機能を使用できるようにする
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm#ユーザー名とパスワードの入力確認や、パスワードが正しく入力されているかの確認機能を利用するため、Djangoに用意されているユーザー登録用フォームを読み込む
from django.contrib.auth.models import User #アカウント登録フォームで入力されたユーザー名やメールアドレスなどを保存できるようにするため、Djangoに用意されているユーザー情報を管理する機能を読み込む
class SignUpForm(UserCreationForm): # Djangoのユーザー登録フォームをもとに、ズボラ飯セレクター用のアカウント登録フォームを作る
    email = forms.EmailField(
        label="メールアドレス",
        required=True
    )  # メールアドレスの入力欄を作り、入力を必須にする
    
    username = forms.CharField(
        label="ユーザー名",
        error_messages={
            "required": "ユーザー名を入力してください。"
        }
    )

    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="パスワード再入力",
        widget=forms.PasswordInput,
        error_messages={
            "required": "パスワードを再入力してください。",
        }
    )
    
    # 同じユーザー名がすでに登録されていないか確認する
    def clean_username(self):

        # 入力されたユーザー名を取得する
        username = self.cleaned_data.get("username")

        # 同じユーザー名がすでに存在する場合はエラーにする
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "このユーザー名はすでに使用されています。"
            )

        return username
    
    # 同じメールアドレスがすでに登録されていないか確認する
    def clean_email(self):

        # 入力されたメールアドレスを取得する
        email = self.cleaned_data.get("email")

        # 同じメールアドレスのユーザーがすでに存在する場合
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "このメールアドレスはすでに登録されています。"
            )

        # 重複していなければ入力されたメールアドレスを返す
        return email
    
    # パスワードが設定条件を満たしているか確認する
    def clean_password1(self):

        # 入力されたパスワードを取得する
        password1 = self.cleaned_data.get("password1")
        
        # パスワードが入力されていない場合は、そのまま返す
        if not password1:
            return password1

        # 8文字未満の場合はエラーにする
        if len(password1) < 8:
            raise forms.ValidationError(
                "パスワードは8文字以上で入力してください。"
            )

        # 大文字が含まれていない場合はエラーにする
        if not re.search(r"[A-Z]", password1):
            raise forms.ValidationError(
                "パスワードには英字の大文字を含めてください。"
            )

        # 小文字が含まれていない場合はエラーにする
        if not re.search(r"[a-z]", password1):
            raise forms.ValidationError(
                "パスワードには英字の小文字を含めてください。"
            )

        # 数字が含まれていない場合はエラーにする
        if not re.search(r"[0-9]", password1):
            raise forms.ValidationError(
                "パスワードには数字を含めてください。"
            )

        return password1
    
    # パスワードとパスワード再入力が一致しているか確認する
    def clean_password2(self):

        # 入力された2つのパスワードを取得する
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # 2つのパスワードが一致していない場合はエラーにする
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "パスワードが一致していません。"
            )

        return password2

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2") #ユーザー名・メールアドレス・パスワードを新しいユーザー情報として登録できるようにするため、アカウント登録フォームで使用するユーザー情報の保存先とフォームに表示する入力項目を設定する
        
from django import forms
from django.contrib.auth.models import User

class AccountEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="メールアドレス",
        required=True,
        error_messages={
            "required": "メールアドレスを入力してください。",
        }
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    # 入力されたユーザー名が他のユーザーに使われていないか確認する
    def clean_username(self):

        # 入力されたユーザー名を取得する
        username = self.cleaned_data.get("username")

        # 自分以外のユーザーで、同じユーザー名が登録されていないか確認する
        if User.objects.filter(
            username=username
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "このユーザー名はすでに登録されています。"
            )

        return username

    # 入力されたメールアドレスが他のユーザーに使われていないか確認する
    def clean_email(self):

        # 入力されたメールアドレスを取得する
        email = self.cleaned_data.get("email")

        # 自分以外のユーザーで、同じメールアドレスが登録されていないか確認する
        if User.objects.filter(
            email=email
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "このメールアドレスはすでに登録されています。"
            )

        return email
    
# パスワード変更フォーム
class CustomPasswordChangeForm(PasswordChangeForm):

    # 入力されたパスワード全体を確認する
    def clean(self):

        # Django標準のパスワードチェックを先に行う
        cleaned_data = super().clean()

        # 入力された新しいパスワードを取得する
        new_password1 = cleaned_data.get("new_password1")

        # 新しいパスワードが入力されている場合
        if new_password1:

            # 8文字未満の場合はエラーにする
            if len(new_password1) < 8:
                self.add_error(
                    "new_password1",
                    "パスワードは8文字以上で入力してください。"
                )

            # 大文字が含まれていない場合はエラーにする
            if not re.search(r"[A-Z]", new_password1):
                self.add_error(
                    "new_password1",
                    "パスワードには英字の大文字を含めてください。"
                )

            # 小文字が含まれていない場合はエラーにする
            if not re.search(r"[a-z]", new_password1):
                self.add_error(
                    "new_password1",
                    "パスワードには英字の小文字を含めてください。"
                )

            # 数字が含まれていない場合はエラーにする
            if not re.search(r"[0-9]", new_password1):
                self.add_error(
                    "new_password1",
                    "パスワードには数字を含めてください。"
                )

            # 新しいパスワードが現在のパスワードと同じ場合はエラーにする
            if self.user.check_password(new_password1):
                self.add_error(
                    "new_password1",
                    "現在のパスワードと異なるパスワードを設定してください。"
                )

        return cleaned_data
    
# パスワードリセット後の新しいパスワード設定フォーム
class CustomSetPasswordForm(SetPasswordForm):

    # 入力されたパスワード全体を確認する
    def clean(self):

        # Django標準のパスワードチェックを先に行う
        cleaned_data = super().clean()

        # 入力された新しいパスワードを取得する
        new_password1 = cleaned_data.get("new_password1")

        # 新しいパスワードが入力されている場合
        if new_password1:

            # 8文字未満の場合はエラーにする
            if len(new_password1) < 8:
                self.add_error(
                    "new_password1",
                    "パスワードは8文字以上で入力してください。"
                )

            # 大文字が含まれていない場合はエラーにする
            if not re.search(r"[A-Z]", new_password1):
                self.add_error(
                    "new_password1",
                    "パスワードには英字の大文字を含めてください。"
                )

            # 小文字が含まれていない場合はエラーにする
            if not re.search(r"[a-z]", new_password1):
                self.add_error(
                    "new_password1",
                    "パスワードには英字の小文字を含めてください。"
                )

            # 数字が含まれていない場合はエラーにする
            if not re.search(r"[0-9]", new_password1):
                self.add_error(
                    "new_password1",
                    "パスワードには数字を含めてください。"
                )

        return cleaned_data