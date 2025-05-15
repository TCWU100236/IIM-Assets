from django.shortcuts import render
from mysite import models

# Create your views here.
def index(request):
    assets = models.Asset.objects.all()
    return render(request, "index.html", locals())

def detail(request, id):
    try:
        asset = models.Asset.objects.get(id=id)
    except:
        pass
    return render(request, "detail.html", locals())