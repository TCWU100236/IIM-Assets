from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class AssetUserProfile(models.Model):
    userid = models.CharField(max_length=10, unique=True, verbose_name="使用者編號")
    username = models.CharField(max_length=10, verbose_name="使用者名稱")

    def __str__(self):
        return f"{self.username}"

class Asset(models.Model):
    ASSET_TYPE_CHOICES = [
        ('財產', '財產'),
        ('非消耗品', '非消耗品'),
    ]

    asset_code = models.CharField(max_length=20, unique=True, verbose_name="財編")
    name = models.CharField(max_length=20, verbose_name="品名")
    accessories = models.TextField(blank=True, null=True, default="暫無附件", verbose_name="附件")
    unit_price = models.PositiveIntegerField(default=0, verbose_name="單價")
    brand = models.CharField(max_length=10, blank=True, null=True, verbose_name="廠牌")
    model = models.CharField(max_length=50, blank=True, null=True, verbose_name="型號")
    origin_country = models.CharField(max_length=10, blank=True, null=True, verbose_name="國別")
    serial_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="序號")
    user = models.ForeignKey(AssetUserProfile, on_delete=models.CASCADE, verbose_name="使用者")
    location = models.CharField(max_length=20, blank=True, null=True, verbose_name="存放處所")
    lifespan_years = models.PositiveIntegerField(default=0, verbose_name="使用年限")
    funding_source = models.CharField(max_length=10, default="不知", verbose_name="經費來源")
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, verbose_name="財產類別")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="購入日期")
    note = models.TextField(blank=True, null=True, verbose_name="備註")

    def __str__(self):
        return f"{self.asset_code} - {self.name}"

class SystemUser(models.Model):
    ROLE_TYPE_CHOICES = [
        ('系統管理者', '系統管理者'),
        ('一般使用者', '一般使用者'),
    ]

    name = models.CharField(max_length=20, null=False, verbose_name="使用者名稱")
    email = models.EmailField(verbose_name="使用者信箱")
    password = models.CharField(max_length=20, null=False, verbose_name="使用者密碼")
    room = models.CharField(max_length=20, null=True, verbose_name="實驗室之編號")
    role = models.CharField(max_length=10, choices=ROLE_TYPE_CHOICES, null=False, default="一般使用者", verbose_name="使用者權限")
    enabled = models.BooleanField(default=False, verbose_name="帳號啟用")

    def __str__(self):
        return f"{self.name} - {self.role}"