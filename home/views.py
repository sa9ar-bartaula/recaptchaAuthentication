from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import requests

from home.forms import UserCreateForm
from home.models import Person

# Create your views here.

RECAPTCHA_SITE_KEY = settings.GOOGLE_RECAPTCHA_SITE_KEY
RECAPTCHA_SECRET_KEY = settings.GOOGLE_RECAPTCHA_SECRET_KEY

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    except Exception as e:
        return None

def index_view(request):
    return render(request, 'index.html')


def register_view(request):
    
    context = {}
    
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
                
            ''' reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            recaptach_verify = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = recaptach_verify.json()
            
            if result['success']:
                user_instance = form.save()
                if user_instance:
                    username = request.POST.get('username')
                    password = request.POST.get('password1')
                    print(f"User successfully registered; '{username}'. ")
                    
                    user = authenticate(request, username=username, password=password)
                    if user:
                        login(request, user)
                        messages.success(request, 'Registration Successfull.',  extra_tags='success')
                        print('User logged in.')
                        return redirect('user_dashboard_url')
            else:
                context = {"error": "Invalid Captcha !!"}
                messages.warning(request, 'reCaptcha verification failed.', extra_tags='warning')
                return render(request, "register.html", context)
        else:
            context = { 'error': form.errors }
            messages.error(request, 'Sorry, an error occured. Please try again.', extra_tags='error')
            
    return render(request, 'register.html', context)


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('user_dashboard_url')
    else:
        context = {}
        
        if request.method == "POST":
            post_request = request.POST
                
            ''' reCAPTCHA validation '''
            recaptcha_response = post_request.get('g-recaptcha-response')
            data = {
                'secret': RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            recaptach_verify = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = recaptach_verify.json()

            if result['success']:
                username = post_request.get('username')
                password = post_request.get('password')
                
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, 'Successfully logged in.', extra_tags='success')
                    print(f"User successfully logged in; '{username}'. ")
                    return redirect('user_dashboard_url')
                else:
                    context = {"error": "Invalid Credentials !!"}
                    messages.error(request, 'This account cannot be found.', extra_tags='error')
                    return render(request, "login.html", context)
            else:
                context = {"error": "Invalid Captcha !!"}
                messages.warning(request, 'reCaptcha verification failed.', extra_tags='warning')
                return render(request, "login.html", context)
            
        return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login_url')


@login_required(login_url='/login/')
def user_dashboard_view(request):
    user = get_or_none(User, id=request.user.id)
    person = get_or_none(Person, user=user)
    profile_complete = False
    profile_data = ''
    if person:
        profile_complete = True
        p = person
        profile_data = {
            'birth_date': p.birth_date,
            'image': p.image.url if p.image else '/static/images/default_img.jpg',
            'gender': p.gender.capitalize(),
            'bio': p.bio,
        }
        print(profile_data)
    
    if request.method == 'POST':
        post_request = request.POST
        birthdate = post_request.get('birthdate')
        gender = post_request.get('gender')
        bio = post_request.get('bio')
        image = request.FILES.get('user_image')
        Person.objects.create(
            user = user,
            birth_date = birthdate,
            image = image,
            gender = gender,
            bio = bio,
        )
        messages.success(request, 'Profile updated successfully.', extra_tags='success')
        return redirect('user_dashboard_url')
        
    context = {
        'user': f'{user.first_name.capitalize()} {user.last_name.capitalize()}',
        'profile_complete': profile_complete,
        'profile': profile_data,
    }
    return render(request, 'user_dashboard.html', context)