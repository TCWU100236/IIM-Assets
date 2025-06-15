from django.shortcuts import render
from mysite import models, forms

# Create your views here.
def index(request):
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
    return render(request, "asset_user.html", locals())

def insert_asset_user(request):
    asset_user_form = forms.UserProfileForm()
    return render(request, "InsertAssetUser.html", locals())

def insert(request):
    asset_form = forms.AssetForm()
    users = models.UserProfile.objects.all()
    return render(request, "insert.html", locals())