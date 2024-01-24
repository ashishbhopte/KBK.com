from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .form import KBKForm  # remember mene form  and model ka nam same diyta hai
from .models import KBKform
import datetime
from django.http import HttpResponse
from django.shortcuts import render, HttpResponse
from django.http import Http404, HttpResponseServerError


def Home(request):
    form = KBKForm()
    return render(request, 'BKB.html', {
        'form': form})  # here we have not mention the path becuase in settings.py we have specified the path of templates file


def SaveForm(request):
    if request.method == "POST":
        form = KBKForm(request.POST)
        try:
            if form.is_valid():
                Name = request.POST.get('Name')
                Email = request.POST.get('Email')
                Phone_no = request.POST.get('Phone_no')
                Url = request.POST.get('Url')
                Company = request.POST.get('Company')
                Date = datetime.datetime.now()
                form_data = KBKform(Name=Name, Email=Email, Phone_no=Phone_no, Url=Url, Company=Company, Date=Date)
                form_data.save()  # This method will save the data
                form = KBKForm()
                return render(request, 'thankyou.html')

        except IntegrityError as e:  # Check if it's a unique constraint violation
            if 'unique constraint' in str(e):
                form.add_error('Url', 'You already used our services')
                return render(request, 'BKB.html', {'form': form})
            else:
                raise e
                return render(request, 'BKB.html', {'form': form})

        except:
            form.add_error('Phone_no', 'Please check the format of the phone no.')
            return render(request, 'BKB.html', {'form': form})


