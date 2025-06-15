from django import forms
from mysite import models

class AssetForm(forms.ModelForm):
    class Meta:
        model = models.Asset
        fields = ["asset_code", "name", "accessories", "unit_price", "brand", "model", "origin_country", "serial_number", "user", "location",
                "lifespan_years", "funding_source", "asset_type", "note"]

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
        self.fields["note"].label = "購入日期"

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ["userid", "username"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["userid"].label = "使用者編號"
        self.fields["username"].label = "使用者名稱"