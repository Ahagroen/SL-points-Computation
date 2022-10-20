from django.shortcuts import redirect, render
from .models import Driver
from .utils import generateDriverInfo,checkValid, tryUpdate

def index(request):
    if request.method == "POST":
        form = request.POST.get("driverName")
        checked_name = checkValid(form)
        if not checked_name:
            return render(request, 'SLdatabase/index.html', {
                'error_message':'Cannot Find that Driver, Check Spelling and try again.'})
        else:
            try:
                driverInfo = Driver.objects.get(name__iexact=checked_name)
                driverInfo = tryUpdate(driverInfo)
            except:
                driverInfo = generateDriverInfo(checked_name)
            return redirect("/SLdatabase/"+str(driverInfo.name))
    else:
        return render(request, 'SLdatabase/index.html', {})

def driverPage(request,driverName):
    driverInfo = Driver.objects.get(name=driverName)
    return render(request,'SLdatabase/driver.html',{'name':driverInfo.name,
        'series':driverInfo.series,'live_points':driverInfo.live_points,'min_points':driverInfo.min_points})
