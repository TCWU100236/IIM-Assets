from django.core.mail import EmailMessage
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from mysite import models, forms
from django.core.paginator import Paginator 

import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
from django.http import HttpResponse

# Create your views here.
def login(request):
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST["username"].strip()
            login_password = request.POST["password"]
            try:
                user = models.SystemUser.objects.get(name = login_name)
                if user.password == login_password:
                    request.session["userid"] = user.id
                    request.session["username"] = user.name
                    request.session["useremail"] = user.email
                    request.session["user_role"] = user.role
                    request.session["stockchecker"] = user.stockchecker.id
                    request.session.set_expiry(1800)    # session 只存活 30 分鐘
                    messages.add_message(request, messages.SUCCESS, "登入成功")
                    return redirect("/")
                else:
                    messages.add_message(request, messages.WARNING, "密碼錯誤，請在檢查一次")
            except:
                messages.add_message(request, messages.WARNING, "找不到使用者")
        else:
            messages.add_message(request, messages.INFO, "請檢查輸入的欄位內容")
    else:
        login_form = forms.LoginForm()
    return render(request, "login.html", locals())

def logout(request):
    if "user_role" in request.session:
        Session.objects.all().delete()
        return redirect("/login/")
    return redirect("/")

def index(request):
    if "user_role" in request.session and request.session["user_role"] != None:
        username = request.session["username"]
        useremail = request.session["useremail"]
        user_role = request.session["user_role"]
        user_stockchecker = request.session["stockchecker"]
    else:
        return redirect("/login/")

    # 取得 GET 參數
    asset_type = request.GET.get("asset_type")
    search_asset_id = request.GET.get("search_asset_id")
    selected_user_id = request.GET.get("user_id")  # 僅供系統管理者用
    # user_id = user_stockchecker

    if user_role == "系統管理者":
        asset_users = models.AssetUserProfile.objects.all()
    else:
        asset_users = models.AssetUserProfile.objects.filter(stockchecker=user_stockchecker)

    # 建立查詢集 (QuerySet)
    assets = models.Asset.objects.filter(user__in=asset_users)

    # 套用其他篩選條件
    if asset_type:
        assets = assets.filter(asset_type=asset_type)
    if search_asset_id:
        assets = assets.filter(asset_code__icontains=search_asset_id)

    # 系統管理者：可再依 GET 參數選取某特定使用者
    if user_role == "系統管理者" and selected_user_id:
        assets = assets.filter(user__username=selected_user_id)

    if not assets.exists():
        messages.add_message(request, messages.WARNING, "沒有資料符合查詢條件")
    
    return render(request, "index.html", locals())

def detail(request, id):
    if "user_role" in request.session and request.session["user_role"] != None:
        user_role = request.session["user_role"]
    try:
        asset = models.Asset.objects.get(id=id)
        # qr_data = '{}&{}'.format('This is the qrcode data assets.',asset.asset_code)
        qr_data = f"{asset.asset_code}"
        qrcode_img = get_qrcode_svg(qr_data)
    except:
        pass
    return render(request, "detail.html", locals())

def asset_user(request):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            return redirect("/")
    else:
        return redirect("/login/")

    asset_users = models.AssetUserProfile.objects.all() # 顯示所有使用者
    paginator = Paginator(asset_users, 10)  # 每頁顯示10筆資料
    page_number = request.GET.get('page')  # 從 URL 取得目前頁數
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        mode = request.POST.get("mode")
        userid = request.POST.get("userid")
        username = request.POST.get("username")

        if mode == "edit":
            original_userid = request.POST.get("original_userid")
            try:
                user = models.AssetUserProfile.objects.get(userid=original_userid)
                user.userid = userid
                user.username = username
                user.save()
                messages.add_message(request, messages.SUCCESS, "財產使用者資料更新成功")
            except:
                messages.add_message(request, messages.WARNING, "財產使用者資料更新失敗")
        else:  # 新增模式
            if models.AssetUserProfile.objects.filter(userid=userid).exists():
                messages.add_message(request, messages.WARNING, "財產使用者編號已存在，新增失敗")
            else:
                models.AssetUserProfile.objects.create(userid=userid, username=username)
                messages.add_message(request, messages.SUCCESS, "財產使用者新增成功")
        return redirect("/asset_user/")

    return render(request, "asset_user.html", locals())

def del_asset_user(request, userid = None):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            return redirect("/")
    else:
        return redirect("/login/")
    
    if userid:
        try:
            asset_users = models.AssetUserProfile.objects.get(id=userid)
            asset_users.delete()
            messages.add_message(request, messages.SUCCESS, "財產使用者刪除成功")
        except:
            messages.add_message(request, messages.WARNING, "財產使用者刪除失敗")
    return redirect("/asset_user/")

def AssetOperation(request, op = None, asset_code = None):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            return redirect("/")
    else:
        return redirect("/login/")

    asset = None
    asset_users = models.AssetUserProfile.objects.all()

    if request.method == "POST":
        if op == "insert":
            asset = models.Asset()
        elif op == "edit" and asset_code:
            try:
                asset = models.Asset.objects.get(asset_code=asset_code)
                asset.delete()
            except:
                messages.add_message(request, messages.WARNING, "沒有該筆財產/非消耗品，請先新增資料")
                return redirect("/Asset/insert")

            # asset = get_object_or_404(models.Asset, id=assetid)

        asset.asset_code = request.POST.get("asset_code")
        asset.serial_number = request.POST.get("serial_number")
        asset.name = request.POST.get("name")
        asset.user = get_object_or_404(models.AssetUserProfile, username=request.POST.get("user"))
        asset.accessories = request.POST.get("accessories")
        asset.location = request.POST.get("location")
        asset.unit_price = request.POST.get("unit_price") or 0
        asset.lifespan_years = request.POST.get("lifespan_years") or 0
        asset.brand = request.POST.get("brand")
        asset.funding_source = request.POST.get("funding_source")
        asset.model = request.POST.get("model")
        asset.asset_type = request.POST.get("asset_type")
        asset.origin_country = request.POST.get("origin_country")
        asset.purchase_date = request.POST.get("purchase_date") or None
        asset.note = request.POST.get("note")

        try:
            asset.save()
            messages.add_message(request, messages.SUCCESS, "財產/非消耗品 資料已成功儲存")
            return redirect("/")
        except Exception as e:
            messages.add_message(request, messages.WARNING, f"資料儲存失敗：{str(e)}")
    else:
        if op == "edit" and asset_code:
            asset = get_object_or_404(models.Asset, asset_code=asset_code)
            return render(request, "InsertAsset.html", locals())
        elif op == "insert":
            return render(request, "InsertAsset.html", locals())
        else:
            messages.add_message(request, messages.WARNING, "無效的操作")
            return redirect("/")

    # asset_users = models.AssetUserProfile.objects.all() # 用於填表下拉選單
    # if request.method == "POST":
    #     # 取得 POST 資料
    #     asset_code = request.POST.get("asset_code", "").strip()
    #     name = request.POST.get("name", "").strip()
    #     serial_number = request.POST.get("serial_number", "").strip()
    #     user_name = request.POST.get("user", "").strip()
    #     asset_type = request.POST.get("asset_type", "").strip()

    #     # 驗證必要欄位
    #     if not asset_code or not name or not serial_number or not user_name or not asset_type:
    #         messages.add_message(request, messages.WARNING, "請填寫所有必填欄位")
    #         return render(request, "InsertAsset.html", locals())
        
    #     # 驗證 user 是否存在
    #     try:
    #         user = models.AssetUserProfile.objects.get(username=user_name)
    #     except models.AssetUserProfile.DoesNotExist:
    #         messages.add_message(request, messages.WARNING, "找不到指定的使用者")
    #         return render(request, "InsertAsset.html", locals())

    #     # 建立新 Asset 物件
    #     asset = models.Asset(
    #         asset_code=asset_code,
    #         name=name,
    #         serial_number=serial_number,
    #         user=user,
    #         asset_type=asset_type,
    #         accessories=request.POST.get("accessories", "暫無附件"),
    #         unit_price=request.POST.get("unit_price") or 0,
    #         brand=request.POST.get("brand", ""),
    #         model=request.POST.get("model", ""),
    #         origin_country=request.POST.get("origin_country", ""),
    #         location=request.POST.get("location", ""),
    #         lifespan_years=request.POST.get("lifespan_years") or 0,
    #         funding_source=request.POST.get("funding_source", "不知"),
    #         purchase_date=request.POST.get("purchase_date") or None,
    #         note=request.POST.get("note", "")
    #     )

    #     try:
    #         asset.full_clean()  # 執行 model 層級驗證（例如 max_length、PositiveInteger）
    #         asset.save()
    #         messages.add_message(request, messages.SUCCESS, "財產/非消耗品 新增成功")
    #         return redirect("/")  # 成功後導回主畫面
    #     except Exception as e:
    #         messages.add_message(request, messages.WARNING, f"財產/非消耗品 新增失敗：{str(e)}")
    #         return render(request, "InsertAsset.html", locals())

    # return render(request, "InsertAsset.html", locals())

def del_asset(request, assetid = None):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            return redirect("/")
    else:
        return redirect("/login/")

    if assetid:
        try:
            asset = models.Asset.objects.get(id=assetid)
            asset.delete()
            messages.add_message(request, messages.SUCCESS, "財產/非消耗品刪除成功")
        except:
            messages.add_message(request, messages.WARNING, "財產/非消耗品刪除失敗")
    return redirect("/")

def SystemUserInfo(request):
    if "user_role" in request.session and request.session["user_role"] != None:
        userid = request.session["userid"]
        user_role = request.session["user_role"]
        username = request.session["username"]
    else:
        return redirect("/login/")
    try:
        userinfo = models.SystemUser.objects.get(id = userid)
    except:
        pass
    return render(request, "System_UserInfo.html", locals())

def contact(request):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "一般使用者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            return redirect("/")
    else:
        return redirect("/login/")

    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_school = form.cleaned_data["user_school"]
            user_email = form.cleaned_data["user_email"]
            user_message = form.cleaned_data["user_message"]
            messages.add_message(request, messages.SUCCESS, "感謝您的來信，我們會儘速處理您的寶貴意見。")
            return redirect("/")

# ====================================== 寄信功能 ======================================
            mail_body = u'''
使用者名稱：{}
是否在學：{}
電子郵件：{}
反應意見如下：
{}'''.format(user_name, user_school, user_email, user_message)

            email = EmailMessage(   '來自【成大工資管財產管理系統】網站的使用者意見', 
                                    mail_body, 
                                    user_email,
                                    ['r76121243@gs.ncku.edu.tw'])
            email.send()
# ======================================================================================

        else:
            messages.add_message(request, messages.WARNING, "請檢查您輸入的資訊是否正確!")
    else:
        form = forms.ContactForm()
    return render(request, "contact.html", locals())

def get_qrcode_svg(text):
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(text ,image_factory=factory, box_size=30)
    stream = BytesIO()
    img.save(stream)
    base64_image = base64.b64encode(stream.getvalue()).decode()
    return 'data:image/svg+xml;utf8;base64,' + base64_image

def qr_view(request):
    qr_data = '{}&{}'.format('This is the qrcode data guys.','bip-zip')
    qrcode_img = get_qrcode_svg(qr_data)
    return render(request, "qr.html", locals())

def qrcode_reader(img):
    image = Image.open(img).convert('L')
    np_image = np.array(image)
    decoded = decode(np_image)
    if decoded:
        return decoded[0].data.decode("utf-8")
    return False

def qr_scan_view(request):
    if request.method == "POST":
        image = request.POST.get("image")
        if not image:
            messages.add_message(request, messages.WARNING, "未收到圖像資料")
            return render(request, "qrscanner.html", locals())
        
        try:
            image_data = base64.b64decode(image.split(",")[1])
            img = BytesIO(image_data)
            data = qrcode_reader(img)
            if not data:
                messages.add_message(request, messages.WARNING, "該張照片有誤，請重新掃描")
                return render(request, "qrscanner.html", locals())
            
            try:
                asset = models.Asset.objects.get(asset_code=data)
                return redirect(f"/detail/{asset.id}")
            except models.Asset.DoesNotExist:
                messages.add_message(request, messages.WARNING, "該筆資料不存在於資料庫中，請聯絡管理員")
                return render(request, "qrscanner.html", locals())
        except Exception as e:
            messages.add_message(request, messages.WARNING, f"發生錯誤：{str(e)}")
            return render(request, "qrscanner.html", locals())
            
    return render(request, "qrscanner.html", locals())