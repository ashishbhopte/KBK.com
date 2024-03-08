import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import IntegrityError
from .form import KBKForm, Signup, Signin,Changepassword,Forgetpassword  # remember mene form  and model ka nam same diya hai
from .models import KBKform # signup_model
import datetime
from django.contrib.auth.models import User, auth
from django.shortcuts import render, HttpResponse, redirect
from Project_KBK import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import Http404
from django.contrib.auth.models import User
from .models import signup_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
import requests


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
                form_data = KBKform(Name=Name, Email=Email, Phone_no=Phone_no, Url=Url, Company=Company,
                                    Date=Date)  # KBKformis a DB name
                form_data.save()  # This method will save the data
                form = KBKForm()
                return render(request, 'thankyou.html')
            else:
                form.add_error('Invald Form Entry,Please check!')
                return render(request, 'BKB.html', {'form': form})


        except IntegrityError as e:  # Check if it's a unique constraint violation
            if 'unique constraint' in str(e):
                form.add_error('Url', 'You have already used our services!')
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
        form = Signup(request.POST,request.FILES)
        username = request.POST['username']
        email = request.POST['email']
        image = request.FILES['image']

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
            form.save().is_active = False  # this will inactivate the user even user is successfully created, remember in admin area.
            form.save()  # this will give u current user name.
            try:
                auth_tocken = str(uuid.uuid4())
                user = User.objects.get(username=username)
                signup_model_obj = signup_model.objects.create(user=user, auth_tocken=str(auth_tocken),
                                                               is_verified=False,image=image)
                signup_model_obj.save()  # This will store this data in db.(signup_model)
            except Exception as e:
                print(e)

            current_site = get_current_site(
                request)  # Function is used to retrieve the current site from the Site model.
            # print('current_site', current_site)
            domain = current_site.domain
            ## start code for signup 1 mail

            user_email = form.pass_to_email()  # ['this will return the email of user in list data structure and user 1st name']
            subject = "Welcome to BKB Signup!|| Please verify your email!!"
            message = "Dear " + user_email[1] + "!\n\n" + "Please verify the below link:\n" + str(
                domain) + '/activate/' + f'{str(auth_tocken)}' + "\nWelcome to BKB Seo and Web Services, your trusted partner for effective Off-Page SEO services and Web Development!, we specialize in enhancing your online visibility and driving organic traffic to your website through strategic off-page optimization techniques like Link Building , Social media marketing, Local SEO etc." + "\n\n" + "Please click the confirmation link in order to activate  singup." + "\n\n" + "Thanks and Regards, \n" + "BKB SERVICES."
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(user_email[0])]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            messages.info(request,
                          'Your registration has successfully completed please check and verify a email by clicking verification link!')
            return redirect('/signin')
            ## ending code for signup 1 mail
        else:
            form = Signup()
            messages.error(request, 'Please check the form fiels, invalid input!')
            return render(request, 'Signup.html',{'form': form})

    else:
        form = Signup()
        return render(request, 'Signup.html', {'form': form})


# This acivate function creating for html link by click to redirect signin page
def activate(request, auth_tocken):
    try:
        signup_model_obj = signup_model.objects.filter(auth_tocken=auth_tocken).first()  #
        user = User.objects.get(username=signup_model_obj)
        # print(user)
        if signup_model_obj:
            signup_model_obj.is_verified = True
            signup_model_obj.save()
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has successfully verified!, Please sign in!')
            return redirect('/signin')
        else:
            # print('inside the else!')
            messages.error(request, 'Your email has not verified!, Please verify the email and signup again!')
            return redirect('/signup')
    except Exception as e:
        print(e)


def signin(request):
    if request.method == "POST":
        form = Signin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_obj = User.objects.filter(username=username).first()  # This line will filter user from the DB.
            if user_obj is None:
                messages.error(request, "User not found, Please signup!")
                return render(request, 'Signin.html', {'form': form})
            signup_model_obj = signup_model.objects.filter(user=user_obj).first()
            if not signup_model_obj.is_verified:
                messages.error(request, "This object is not at verified, Please verify it by email and signin!")
                return render(request, 'Signin.html', {'form': form})
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Credencials are incorrect please verify and signin again!")
                return render(request, 'Signin.html', {'form': form})
            login(request, user)
            print('user loggnin',user)
            return redirect(f'/afterlogin/{user.username}')
        except:
            messages.error(request, "Something went wrong please check and verify again!")
            return render(request, 'Signin.html', {'form': form})
    else:
        form = Signin()
        return render(request, 'Signin.html', {'form': form})


def signout(request):
    logout(request)
    messages.success(request, "Logged out sucessfully!!")
    return redirect('/')


def afterlogin(request,username):
    user=User.objects.get(username=username)
    user1 = signup_model.objects.get(user_id=user.id)
    print(user1.user,user1.auth_tocken,user1.is_verified,user1.image)
    messages.success(request,f'Welcome back {user.first_name}, \n You have successfully logged in to BKB service and plan section')
    return render(request, 'afterlogin.html')

def forgetpassword(request):
    print('inside forget password')
    if request.method == "POST":
        print('inside if post condition')
        form = Forgetpassword(request.POST) # This will craete the form
        username=request.POST.get('username') # This will take the user which has given in fruntend
        try:
            if not User.objects.filter(username=username).first():
                messages.info(request, 'No user,found with this name')
                return render(request, 'Forgerpassword.html', {'form': form}) # If that user is not present than will return the msg
            else:
                user_obj= User.objects.get(username=username)  # with this line you will get the obj of this user
                print('This is that user:',user_obj.email)
                signup_model_obj = signup_model.objects.get(user=user_obj) # Here basically you are getting this obj for signup_model model.
                token = str(uuid.uuid4())  # this will create the random token
                signup_model_obj.auth_tocken = token
                signup_model_obj.save()
                # ### This below line will send the email for forget password:
                current_site = get_current_site(request)
                domain = current_site.domain
                subject = "Reset Password for BKB SEOANDWEB!"
                message = "Dear " + user_obj.first_name + "!\n\n" + "Please click the below reset password page:\n" + str(domain) + '/resetpassword/' + f'{str(token)}' +"\n\n" + "Thanks and Regards, \n" + "BKB SERVICES."
                from_email = settings.EMAIL_HOST_USER
                to_list = [str(user_obj.email)]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
                messages.info(request, f'{user_obj.first_name} We have sent a forget password link to your email please check!'.format())
                return render(request, 'Forgerpassword.html', {'form': form})

        except Exception as e:
            print(e)

    else:
        form = Forgetpassword()
        return render(request,'Forgerpassword.html',{'form':form})

def resetpassword(request,token):
    if request.method == "GET":
        signup_mode_obj= signup_model.objects.get(auth_tocken=token)
        form = Changepassword()
        return render(request, 'Changepassword.html', {'form': form,'user_id':signup_mode_obj.user.id}) #from here you are passing the user_id as well

    elif request.method == "POST":
        new_password=request.POST.get('password1') # from frunt end we havce taken the password1
        confirm_password=request.POST.get('password2') # from frunt end we havce taken the patake2
        user_id=request.POST.get('user_id')
        user_obj = User.objects.get(id=user_id)
        if new_password != confirm_password:
            messages.error(request, 'Password have not matched.')
            return redirect(f'/resetpassword/{token}/')
        elif user_id is None:
            messages.error(request,'No user ID found, Please try again')
            return redirect(f'/resetpassword/{token}/')

        elif user_obj.password == new_password:
            messages.error(request, 'You already used this password please with different')
            return redirect(f'/resetpassword/{token}/')

        else:
            user_obj.set_password(new_password)
            user_obj.save()
            messages.info(request, 'your password has successfully changed, Please login')
            return redirect('/signin')
    else:
        form = Changepassword()
        return render(request, 'Changepassword.html', {'form': form})

