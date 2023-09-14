from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        fields = ["email"]

    password = None


class UserUpdateForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        fields = ["username", "email", "is_superuser"]

    password = None


class UserCreationForm(auth_forms.UserCreationForm):

    error_message = auth_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "is_superuser"]

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserUpdateListForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "is_superuser"]

    username = forms.CharField(disabled=True)
    password = None


UserFormSet = forms.modelformset_factory(
    User, form=UserUpdateListForm, extra=0, can_delete=False
)
