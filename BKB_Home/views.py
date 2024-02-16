from Tools.scripts import generate_token
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import IntegrityError
from .form import KBKForm, Signup, Signin # remember mene form  and model ka nam same diyta hai
from .models import KBKform
import datetime
from django.contrib.auth.models import User, auth
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from Project_KBK import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.http import Http404, HttpResponseServerError
# from .tockens import generate_token
from email.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
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
        if User.objects.filter(username=username):
            messages.error(request, "Entered user name is already exist, Please try with other user name!")
            return redirect('/signup')
        if len(username) > 15:
            messages.error(request, "User name should be less than 10 character!")
            return redirect('/signup')
        if not username.isalnum():
            messages.error(request, "User name should alpha numeric !")
            return redirect('/signup')
        if User.objects.filter(email=email):
            messages.error(request, "User email is already exist, Please login with this email or forger password!")
            return redirect('/signin')


        if form.is_valid():
            form.save().is_active=False # this will inctive the user even user is successfully created.
            form.save() # this will give u current user name.
            messages.success(request,"Your account has successfully register, Please verift the gmail by clicking the verification link in order to successfull Signup!!")

            ## start code for signup 1 mail: welcome to BKB services check the confirmation mail.

            user_email = form.pass_to_email()  # ['this will return the email of user in list data structure and user 1st name']
            subject = "Welcome to BKB signup!!!"
            message = "Dear " + user_email[1] + "!," + "\nWelcome to BKB Seo and Web Services, your trusted partner for effective Off-Page SEO services!, we specialize in enhancing your online visibility and driving organic traffic to your website through strategic off-page optimization techniques like Link Building , Social media marketing, Local SEO etc."+"\n\n" + "Please check the confirmation mail and click on confirmation link in order to activate singup" + "\n\n" + "Thanks and Regards, \n" + "BKB SERVICES."
            from_email = settings.EMAIL_HOST_USER
            to_list=[str(user_email[0])]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            return redirect('/signin')

            ## ending code for signup 1 mail: welcome to BKB services check the confirmation mail.


            ## starting code for signup 2 mail: cnfirmation mail link.
            current_site = get_current_site(request)
            email_subject = "Please confirm your email authentication @BKB Services!"
            messages2 = render_to_string('email_confirmation.html',{
                'name': user_email[1],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(form.save().pk)), ###yha per may be I will gwr some error
                'token': generate_token.make_token(form.save())
            })
            email= EmailMessage(
                email_subject,
                messages2,
                settings.EMAIL_HOST_USER,
                [str(user_email[0])],

            )
            email.fail_silentl=True
            email.send()

            ## ending code for signup 2 mail: confirmation mail link.

    else:
        form = Signup()
    return render(request, 'Signup.html', {'form': form})

# This acivate function creating for html link by click to redirect signin page
def acivate(request, uidb64, token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except( TypeError, ValueError,OverflowError,User.DoesNotExist):
        myuser= None
    if myuser is not None:
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
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

