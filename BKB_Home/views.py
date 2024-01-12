from django.shortcuts import render
from .models import KBKform
import datetime
from django.http import HttpResponse


def Home(request):
    return render(request,'BKB.html')  # here we have not mention the path becuase in settings.py we have specified the path of templates file


def SaveForm(request):
    print('saveform intial phase')
    msg=''
    if request.method == "POST":
        print('line16')
        Name = request.POST.get('Name')
        print('This is name',Name)
        Email = request.POST.get('Email')
        Phone_no = request.POST.get('Phone_no')
        Url = request.POST.get('Url')
        Company = request.POST.get('Company')
        Date = datetime.datetime.now()
        # print("This is date time", Date)
        form_data = KBKform(Name=Name, Email=Email, Phone_no=Phone_no, Url=Url, Company=Company, Date=Date)
        form_data.save() # This method will save the data
        msg= 'Thankyou for choosing us, we will soon send you analyse report!'
        print('saveform last line')
    return render(request, 'thankyou.html')  # msg--> yha per msg bhi pass ker diya hai jo html me print ker dunga