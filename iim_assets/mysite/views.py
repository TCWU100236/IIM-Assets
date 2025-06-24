from django.contrib.sessions.models import Session
from django.contrib import messages
from django.shortcuts import render, redirect
from mysite import models, forms

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
                    request.session["room"] = user.room
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
        user_room = request.session["room"]
    else:
        return redirect("/login/")

    # 取得 GET 參數
    asset_type = request.GET.get("asset_type")
    search_asset_id = request.GET.get("search_asset_id")
    user_id = user_room

    if user_role == "系統管理者":
        asset_users = models.AssetUserProfile.objects.all()
        user_id = request.GET.get("user_id")

    # 建立查詢集 (QuerySet)
    assets = models.Asset.objects.all()
    if asset_type:
        assets = assets.filter(asset_type=asset_type)
    if search_asset_id:
        assets = assets.filter(asset_code__icontains=search_asset_id)
    if user_id:
        assets = assets.filter(user__username__icontains=user_id)

    if not assets.exists():
        messages.add_message(request, messages.WARNING, "沒有資料符合查詢條件")
    
    return render(request, "index.html", locals())

def detail(request, id):
    if "user_role" in request.session and request.session["user_role"] != None:
        user_role = request.session["user_role"]
    try:
        asset = models.Asset.objects.get(id=id)
    except:
        pass
    return render(request, "detail.html", locals())

def asset_user(request):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            Session.objects.all().delete()
            return redirect("/login/")
    else:
        return redirect("/login/")

    asset_users = models.AssetUserProfile.objects.all() # 顯示所有使用者
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
            Session.objects.all().delete()
            return redirect("/login/")
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

def AssetOperation(request, op = None, assetid = None):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            Session.objects.all().delete()
            return redirect("/login/")
    else:
        return redirect("/login/")

    if op == "insert":
        print("新增資料")
    elif op == "edit" and assetid:
        print("修改資料")
        try:
            asset = models.Asset.objects.get(id=assetid)
            asset_code
        except:
            messages.add_message(request, messages.WARNING, "找不到該筆財產/非消耗品，請新增資料")
        return render(request, "InsertAsset.html", locals())
    else:
        print("沒有動作")

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

    return render(request, "InsertAsset.html", locals())

def del_asset(request, assetid = None):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            Session.objects.all().delete()
            return redirect("/login/")
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