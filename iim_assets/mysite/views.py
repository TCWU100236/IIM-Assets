from django.shortcuts import render, redirect
from mysite import models, forms

# Create your views here.
def index(request):
    users = models.UserProfile.objects.all()

    # 取得 GET 參數
    asset_type = request.GET.get("asset_type")
    search_asset_id = request.GET.get("search_asset_id")
    user_id = request.GET.get("user_id")

    # 建立查詢集（QuerySet）
    assets = models.Asset.objects.all()
    if asset_type:
        assets = assets.filter(asset_type=asset_type)
    if search_asset_id:
        assets = assets.filter(asset_code__icontains=search_asset_id)
    if user_id:
        assets = assets.filter(user__userid__icontains=user_id)

    message = None if assets.exists() else "查無符合條件的財產"
    
    return render(request, "index.html", locals())

def detail(request, id):
    try:
        asset = models.Asset.objects.get(id=id)
    except:
        pass
    return render(request, "detail.html", locals())

def asset_user(request):
    asset_users = models.UserProfile.objects.all()

    if request.method == "POST":
        asset_user_form = forms.UserProfileForm(request.POST)
        if asset_user_form.is_valid():
            asset_user_form.save()
            return redirect("/asset_user/")
        else:
            message = "財產使用者新增失敗"
    else:
        asset_user_form = forms.UserProfileForm()

    return render(request, "asset_user.html", locals())

def asset_insert(request):
    message = ""
    if request.method == "POST":
        asset_form = forms.AssetForm(request.POST)
        if asset_form.is_valid():
            asset_form.save()
            return redirect("/")
        else:
            message = "資料有錯，請再檢查一次"
            for field, errors in asset_form.errors.items():
                for error in errors:
                    message += f"\n{field}: {error}"
    else:
        asset_form = forms.AssetForm()
    return render(request, "InsertAsset.html", locals())