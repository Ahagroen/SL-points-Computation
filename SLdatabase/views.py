from django.shortcuts import redirect, render
from .models import Driver
from .utils import scanDatabaseName, tryUpdate

def index(request):
    if request.method == "POST":
        form = request.POST.get("driverName")
        Name = scanDatabaseName(form)
        if Name:
            driverInfo = Driver.objects.get(name=Name)
            driverInfo = tryUpdate(driverInfo)
            return redirect("/SLdatabase/"+str(driverInfo.name))
        else:
            return render(request, 'SLdatabase/index.html', {
                'error_message':'Cannot Find that Driver, Check Spelling and try again.'}) #Fix back button so that it doesn't render this error message
    else:
        return render(request, 'SLdatabase/index.html', {})

def driverPage(request,driverName):
    driverInfo = Driver.objects.get(name=driverName)
    return render(request,'SLdatabase/driver.html',{'name':driverInfo.name,
        'seriesList':list(driverInfo.racingseries_set.all().order_by("-year"))[0:11],'live_points':driverInfo.live_points,'min_points':driverInfo.min_points})
