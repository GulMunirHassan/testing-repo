from django import forms

class LoginForm(forms.Form):
    ID_Number = forms.CharField()
    PIN_Password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    UserName = forms.CharField()
    ID_Number = forms.CharField()
    MobileNumber = forms.CharField()
    PIN_Password = forms.CharField(widget=forms.PasswordInput)
    IsOTP_Enabled = forms.BooleanField(required=False)
    ResidentTypeID = forms.IntegerField()
    ResellerID = forms.IntegerField()

