from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm


class SelfLoginForm(LoginForm):
    """Remove labels in allauth forms"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].label = ""
        self.fields["password"].label = ""


class SelfSignupForm(SignupForm):
    """Remove labels in allauth forms"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = ""
        self.fields["username"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""


class SelfResetPasswordForm(ResetPasswordForm):
    """Remove labels in allauth forms"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = ""
