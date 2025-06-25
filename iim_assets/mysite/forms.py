from django import forms
from mysite import models
from captcha.fields import CaptchaField

class AssetForm(forms.ModelForm):
    class Meta:
        model = models.Asset
        fields = ["asset_code", "name", "accessories", "unit_price", "brand", "model", "origin_country", "serial_number", "user", "location",
                "lifespan_years", "funding_source", "asset_type", "purchase_date", "note"]

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields["asset_code"].label = "財產編號"
        self.fields["name"].label = "品名"
        self.fields["accessories"].label = "附件"
        self.fields["unit_price"].label = "單價"
        self.fields["brand"].label = "廠牌"
        self.fields["model"].label = "型號"
        self.fields["origin_country"].label = "國別"
        self.fields["serial_number"].label = "序號"
        self.fields["user"].label = "使用者"
        self.fields["location"].label = "存放處所"
        self.fields["lifespan_years"].label = "使用年限"
        self.fields["funding_source"].label = "經費來源"
        self.fields["asset_type"].label = "財產類別"
        self.fields["purchase_date"].label = "購入日期"
        self.fields["note"].label = "備註"

class AssetUserProfileForm(forms.ModelForm):
    class Meta:
        model = models.AssetUserProfile
        fields = ["userid", "username"]

    def __init__(self, *args, **kwargs):
        super(AssetUserProfileForm, self).__init__(*args, **kwargs)
        self.fields["userid"].label = "使用者編號"
        self.fields["username"].label = "使用者名稱"

class LoginForm(forms.Form):
    username = forms.CharField(label="使用者名稱", max_length=20)
    password = forms.CharField(label="密碼", widget=forms.PasswordInput())

class ContactForm(forms.Form):
    user_name = forms.CharField(label="您的使用者名稱", max_length=20, initial="李大仁")
    user_school = forms.BooleanField(label='是否在學', required=False)
    user_email = forms.EmailField(label='電子郵件')
    user_message = forms.CharField(label='您的意見', widget=forms.Textarea)
    captcha = CaptchaField(label="請輸入驗證碼")