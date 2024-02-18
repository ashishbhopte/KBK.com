import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import IntegrityError
from .form import KBKForm, Signup, Signin # remember mene form  and model ka nam same diya hai
from .models import KBKform,signup_model
import datetime
from django.contrib.auth.models import User, auth
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from Project_KBK import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.http import Http404
from django.contrib.auth.models import User
from . models import signup_model
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
                form_data = KBKform(Name=Name, Email=Email, Phone_no=Phone_no, Url=Url, Company=Company, Date=Date) # KBKformis a DB name
                form_data.save()  # This method will save the data
                form = KBKForm()
                return render(request, 'thankyou.html')
            else:
                form.add_error('Invald Form Entry,Please check!')
                return render(request, 'BKB.html', {'form': form})


        except IntegrityError as e:  # Check if it's a unique constraint violation
            if 'unique constraint' in str(e):
                form.add_error('Url', 'You already used our services')
                return render(request, 'BKB.html', {'form': form})
            else:
                raise e
                return render(request, 'BKB.html', {'form': form})
        except ValueError:
            return render(request, 'BKB.html', {'form': form})

        except:
            # form.add_error('Phone_no', 'Please check the format of the phone no.')
            return render(request, 'BKB.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = Signup(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(email=email):
            messages.error(request, "User email is already exist, Please login with this email or forger password!")
            return redirect('/signin')
        if User.objects.filter(username=username):
            messages.error(request, "Entered user name is already exist, Please try with other user name!")
            return redirect('/signup')
        if len(username) > 15:
            messages.error(request, "User name should be less than 10 character!")
            return redirect('/signup')
        if not username.isalnum():
            messages.error(request, "User name should alpha numeric !")
            return redirect('/signup')
        if form.is_valid():
            form.save().is_active=False # this will inactive the user even user is successfully created, remember in admin area.
            form.save() # this will give u current user name.
            try:
                user = User.objects.get(username=username)
                signup_model_obj = signup_model.objects.create(user=user, auth_tocken=str(uuid.uuid4()), is_verified=False)
                signup_model_obj.save()  # This will store this data in db.(signup_model)
            except Exception as e:
                print(e)

            ## start code for signup 1 mail
            user_email = form.pass_to_email()  # ['this will return the email of user in list data structure and user 1st name']
            subject = "Welcome to BKB Signup!|| Please verify your email!!"
            message = "Dear " + user_email[1] + "!\n\n" +"Please verify the below link:\n"+"\nWelcome to BKB Seo and Web Services, your trusted partner for effective Off-Page SEO services!, we specialize in enhancing your online visibility and driving organic traffic to your website through strategic off-page optimization techniques like Link Building , Social media marketing, Local SEO etc."+"\n\n" + "Please check the confirmation mail and click on confirmation link in order to activate singup" + "\n\n" + "Thanks and Regards, \n" + "BKB SERVICES."
            from_email = settings.EMAIL_HOST_USER
            to_list=[str(user_email[0])]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            messages.success(request,'Your registtion has successfully completed please chaeck and verify a email by clicking verification link!')
            return redirect('/signin')

            ## ending code 1 mail

    else:
        form = Signup()
    return render(request, 'Signup.html', {'form': form})

# This acivate function creating for html link by click to redirect signin page
def activate(request, uidb64, token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except( TypeError, ValueError,OverflowError,User.DoesNotExist):
        myuser= None
    if myuser is not None:
        myuser.is_active = True
        myuser.save()
        messages.success(request,'your gmail has verified and your account is activatd now!,Please login')
        return redirect('/signin')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None: # after successfull authentication
            login(request, user)
            uname=user.first_name
            return render(request,'afterlogin.html',{'uname':uname})
        else: # if credential will not match
            messages.error(request,"your username and password is wrong!")
            return redirect('/signin')
    else:
        form = Signin()
    return render(request, 'Signin.html', {'form': form})


def signout(request):
    logout(request)
    messages.success(request,"Logged out sucessfully!!!")
    return redirect('/')

