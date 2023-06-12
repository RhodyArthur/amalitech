from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
import string
import random
from .models import AccessKey
from .forms import AccessKeyForm, UserRegistrationForm
from verify_email.email_handler import send_verification_email

# Create your views here.

#dashboard
@login_required
def homePage(request):
    return render(request, 'base/home.html', {'section':'homePage'})

# register 
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new user object
            new_user = user_form.save(commit=False)
            #set password
            new_user.set_password(
                user_form.cleaned_data['password'])
            #save the user object
            new_user = send_verification_email(request, user_form)
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'user_form':user_form})

# display list of keys
@login_required
def access_key_list(request):
    if request.user.is_staff:
        access_keys = AccessKey.objects.order_by('status', 'user', '-date_procured')
    else:
        access_keys = AccessKey.objects.filter(user=request.user).order_by('status', 'user',  '-date_procured')
    return render(request, 'base/access_key_list.html', {'access_keys': access_keys})

#key generation function
def generate_access_key(length=16):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(length))
    return key


@login_required
def GenerateAccessKeyView(request):
    if request.method == "POST":
        form = AccessKeyForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            form.cleaned_data['status']
            form.cleaned_data['expiry_date']

            existing_active_keys = AccessKey.objects.filter(user=user, status='active')

            if existing_active_keys.exists():
                error_message = 'An active access key already exists for this user.'
                return render(request, 'base/access_key_list.html', {'form': form, 'error_message': error_message})

            access_key = generate_access_key()
            form.instance.key_value = access_key
            access_key = form.save()
            return redirect('access_key_list')  # Redirect to the access key list page
        
        return render(request, 'base/generate_access_key.html', {'form': form})
    else:
        form = AccessKeyForm()
    return render(request, 'base/generate_access_key.html', {'form': form})

# ADMIN
@login_required
@staff_member_required
def admin_dashboard(request):
    access_keys = AccessKey.objects.order_by('status', 'user', '-date_procured')
    context = {'access_keys': access_keys}
    return render(request, 'base/admin_dashboard.html', context)


# revoke access key
@login_required
@staff_member_required
def revoke_access_key(request, pk):
    access_key = AccessKey.objects.get(id=pk)

    if request.method == 'POST':
        access_key.status = 'revoked'
        access_key.save()
        return redirect(reverse('admin_dashboard'))
    return render(request, 'base/revoke_key.html',{'access_key':access_key})

@login_required
@staff_member_required
def school_key_details(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if email:
            try:
                access_key = AccessKey.objects.get(user__email=email, status='active')
                return JsonResponse({
                    'status': 200,
                    'key_value': access_key.key_value,
                    'date_procured': access_key.date_procured,
                    'expiry_date': access_key.expiry_date
                })
            except AccessKey.DoesNotExist:
                return JsonResponse({'status': 404}, status=404)
        return render(request, 'base/school_key_details_form.html')
    