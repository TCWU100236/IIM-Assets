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

    asset_users = models.AssetUserProfile.objects.all()

    if request.method == "POST":
        asset_user_form = forms.AssetUserProfileForm(request.POST)
        if asset_user_form.is_valid():
            asset_user_form.save()
            messages.add_message(request, messages.SUCCESS, "財產使用者新增成功")
        else:
            messages.add_message(request, messages.WARNING, "財產使用者新增失敗")
        return redirect("/asset_user/")
    else:
        asset_user_form = forms.AssetUserProfileForm()

    return render(request, "asset_user.html", locals())

def insert_asset(request):
    if "user_role" in request.session and request.session["user_role"] != None:
        if request.session["user_role"] == "系統管理者":
            user_role = request.session["user_role"]
        else:
            messages.add_message(request, messages.WARNING, "您沒有此權限，請聯絡系統管理員")
            Session.objects.all().delete()
            return redirect("/login/")
    else:
        return redirect("/login/")

    if request.method == "POST":
        asset_form = forms.AssetForm(request.POST)
        if asset_form.is_valid():
            asset_form.save()
            return redirect("home")
        else:
            message = "資料有錯，請再檢查一次。"
            for field, errors in asset_form.errors.items():
                for error in errors:
                    message += f"\n{field}: {error}"
    else:
        asset_form = forms.AssetForm()
    return render(request, "InsertAsset.html", locals())

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