from django import forms
from .models import SignUp  # SignUp 모델을 가져옵니다

class loginForms(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class signUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    otpCode = forms.CharField(max_length=16)  # OTP 코드는 6자리로 설정 (필요시 수정 가능)

    class Meta:
        model = SignUp
        fields = ['username', 'name', 'phone', 'email', 'password', 'otpCode']

    # 비밀번호 확인을 위해 clean 메서드 재정의
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        return cleaned_data