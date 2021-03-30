from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from allauth.socialaccount.models import SocialAccount
class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        import quickemailverification
        client = quickemailverification.Client(
            '062bc377edc95eb2242a3a74ab74196575d7febf21eee9e059adadc8eed6')  # Replace API_KEY with your API Key
        quickemailverification = client.quickemailverification()
        # Email address which need to be verified
        response = quickemailverification.verify(email)
        # print(response.body)  # The response is in the body attribute
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            self.add_error(
                'email', 'There is no user registered with the specified email address!')
        if not response.body:
            self.add_error('email', 'Invalid Email Address :(')
        user = User.objects.get(email=email)
        socialinfo=SocialAccount.objects.get(user=user)
        print(socialinfo.provider)
        print(socialinfo.extra_data)
        if socialinfo.provider=='Google':
            self.add_error('email', "Your email is already linked with google")
        return email
