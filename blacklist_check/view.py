from django.contrib.auth.decorators import login_required
from django.shortcuts import render


#@login_required(login_url='/blacklist/login')
def index(request):
    data = dict()
    return render(request, "default/index.html", data)


@login_required(login_url='/blacklist/login')
def ip(request, pk):
    data = dict()
    return render(request, "default/ip.html", data)
