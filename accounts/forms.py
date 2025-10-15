from typing import Any, Optional, cast

from django.contrib.auth.forms import (
    AuthenticationForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.forms import Field
from django.http import HttpRequest

from .models import User


def _update_field_attrs(fields: dict, name: str, attrs: dict[str, Any]) -> None:
    field = cast(Field, fields[name])
    field.widget.attrs.update(attrs)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)

            self.fields["first_name"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "First Name",
                    "required": "True",
                }
            )
            self.fields["last_name"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Last Name",
                    "required": "True",
                }
            )
            self.fields["username"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Username", "required": "True"}
            )
            self.fields["email"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Email", "required": "True"}
            )
            self.fields["password1"].widget.attrs.update(
                {"class": "form-control", "placeholder": "Password", "required": "True"}
            )
            self.fields["password2"].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "Retype Password",
                    "required": "True",
                }
            )


class UserLoginForm(AuthenticationForm):
    def __init__(
        self, request: Optional[HttpRequest] = None, *args: Any, **kwargs: Any
    ) -> None:
        super(UserLoginForm, self).__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username", "required": "True"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-contol", "placeholder": "Password", "required": "True"}
        )


class ResetPasswordConfirmForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]

    def __init__(self, user: User, *args: Any, **kwargs: Any) -> None:
        super().__init__(user, *args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "New Password", "required": True}
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Retype New Password",
                "required": True,
            }
        )
