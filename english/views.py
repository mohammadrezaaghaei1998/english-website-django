from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from learn.models import Video, Purchase ,Package,UserPackage,UserInformation,ContactSubmission
from .forms import PurchaseForm,ContactForm
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from .forms import ChangePasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

from django.views.decorators.http import require_http_methods
import hashlib
import base64
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.parse






def HOME(request):
    packages = Package.objects.all()
    return render(request,'main/home.html', {'packages': packages})



def COURSES(request):
    packages = Package.objects.all()
    return render(request,'main/courses.html', {'packages': packages})




def ABOUT(request):
    return render(request,'main/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email
            submission = ContactSubmission(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            submission.save()

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})





@login_required
def package_detail(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    user_package, created = UserPackage.objects.get_or_create(user=request.user, package=package)
    videos = Video.objects.filter(package=package)

    context = {
        'package': package,
        'videos': videos,
        'user_package': user_package,
    }
    return render(request, 'main/package_detail.html', context)


# def purchase_package(request, package_id):
#     package = get_object_or_404(Package, pk=package_id)
#     form = PurchaseForm(request.POST or None)

#     if request.method == 'POST':
#         if form.is_valid():
#             user = request.user
#             selected_package = form.cleaned_data['package']
#             purchased_videos = Video.objects.filter(package=selected_package)

#             purchase = Purchase.objects.create(user=user, package=selected_package, successful=True)
#             purchase.videos.set(purchased_videos)

#             user_package, created = UserPackage.objects.get_or_create(user=user, package=selected_package)
#             if created:
#                 user_package.unlocked = True
#                 user_package.save()

#             return redirect('payment_success')
#     else:
#         form = PurchaseForm(initial={'package': package})

#     context = {
#         'form': form,
#         'package': package,
#     }

#     return render(request, 'main/purchase_package.html', context)




# def payment_success(request):
#     latest_purchase = Purchase.objects.filter(user=request.user, successful=True).latest('timestamp')
#     selected_package = latest_purchase.package
#     unlocked_videos = latest_purchase.videos.all()

#     context = {
#         'selected_package': selected_package,
#         'unlocked_videos': unlocked_videos,
#     }

#     return render(request, 'main/payment_success.html', context)




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "main/login.html")





def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        try:
            existing_user = User.objects.get(username=username)
            messages.error(request, "Username already taken.")
            return redirect("register")
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            userinfo = UserInformation.objects.create(user=user, first_name=first_name, last_name=last_name, phone_number=phone_number, email=email)
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("home")
    
    return render(request, "main/register.html")




def logout_user(request):
    logout(request)
    return redirect('home')




@login_required
def dashboard(request):
    user_packages = UserPackage.objects.filter(user=request.user)
    change_password_form = PasswordChangeForm(user=request.user)
    try:
        user_information = UserInformation.objects.get(user=request.user)
    except UserInformation.DoesNotExist:
        user_information = None

    context = {
        'user_packages': user_packages,
        'change_password_form': change_password_form,
        'user_information': user_information,
        
    }
    return render(request, 'main/dashboard.html', context)




def packages(request, package_id):
    package = get_object_or_404(Package, pk=package_id)
    
    if request.user.is_authenticated:
        user_package, created = UserPackage.objects.get_or_create(user=request.user, package=package)
    else:
        user_package = None

    context = {
        'package': package,
        'user_package': user_package,
    }

    return render(request, 'main/packages.html', context)




@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password_done')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'main/change_password.html', {'form': form})




def change_password_done(request):
    messages.success(request, 'Your password was successfully updated!')
    return render(request,'main/dashboard.html')





@login_required
def video_list(request):
    user_packages = UserPackage.objects.filter(user=request.user)
    

    context = {
        'user_packages': user_packages,
        
    }
    return render(request, 'main/video_list.html', context)






def index(request,package_id):
    package = None 
    user_package = None 
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        payment_success = process_payment(request.POST)
        
        if payment_success:
            user_info, created = UserInformation.objects.get_or_create(user=request.user)
            user_info.first_name = request.POST.get('first_name')
            user_info.last_name = request.POST.get('last_name')
            user_info.email = request.POST.get('user_email')
            user_info.phone_number = request.POST.get('phone_number')
            user_info.save()

            
            user_package = UserPackage.objects.create(user=request.user, package=package, unlocked=True)
        else:
            return render(request, 'payment_failure.html')

        return redirect('index')
    else: 
        package = Package.objects.get(pk=package_id)  
        context = {
            'package': package,
            'user_package': user_package,
        }

        return render(request, 'index.html', context)
        







SANAL_POS = {
    'customer_id': '400235',
    'merchant_id': '496',
    'username': 'apitest',
    'password': 'api123',
    'ok_url': 'http://127.0.0.1:8000/ok-url/',
    'fail_url': 'http://127.0.0.1:8000/fail-url/',
    'kart_onay_url': 'https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelPayGate',
    'odeme_onay_url': 'https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelProvisionGate',
} # DEBUG == True şeklinde kontrol yaparak prod'a göre conf yapabilirsiniz


@require_http_methods(['POST'])
def odeme(request,package_id):
    if request.method == 'POST':
        
        package = Package.objects.get(pk=package_id)
        user_package = UserPackage.objects.create(user=request.user, package=package, unlocked=False)
        user_info, created = UserInformation.objects.get_or_create(user=request.user)
        user_info.first_name = request.POST.get('first_name')
        user_info.last_name = request.POST.get('last_name')
        user_info.email = request.POST.get('user_email')
        user_info.phone_number = request.POST.get('phone_number')
        user_info.save()

        # return redirect('ok-url')


    name = request.POST.get('name')
    expiry = request.POST.get('expiry').split('/')
    year = expiry[1].strip()
    month = expiry[0].strip()
    number = request.POST.get('number').replace(' ', '')
    cvc = request.POST.get('cvc')
    merchant_order_id = 'web-odeme'
    package = Package.objects.get(pk=package_id)
    tutar = int(package.price * 100)
    hashed_password = base64.b64encode(hashlib.sha1(f"{SANAL_POS['password']}".encode('ISO-8859-9')).digest()).decode()
    hashed_data = base64.b64encode(hashlib.sha1(
        f"{SANAL_POS['merchant_id']}{merchant_order_id}{tutar}{SANAL_POS['ok_url']}{SANAL_POS['fail_url']}{SANAL_POS['username']}{hashed_password}".encode(
            'ISO-8859-9')).digest()).decode()
    data = f"""
        <KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <APIVersion>1.0.0</APIVersion>
    <OkUrl>{str(SANAL_POS["ok_url"])}</OkUrl>
    <FailUrl>{str(SANAL_POS["fail_url"])}</FailUrl>
    <HashData>{hashed_data}</HashData>
    <MerchantId>{int(SANAL_POS['merchant_id'])}</MerchantId>
    <CustomerId>{int(SANAL_POS['customer_id'])}</CustomerId>
    <UserName>{str(SANAL_POS['username'])}</UserName>
    <CardNumber>{str(number)}</CardNumber>
    <CardExpireDateYear>{str(year)}</CardExpireDateYear>
    <CardExpireDateMonth>{str(month)}</CardExpireDateMonth>
    <CardCVV2>{str(cvc)}</CardCVV2>
    <CardHolderName>{str(name)}</CardHolderName>
    <CardType>Troy</CardType>
    <TransactionType>Sale</TransactionType>
    <InstallmentCount>{int('0')}</InstallmentCount>
    <Amount>{int(tutar)}</Amount>
    <DisplayAmount>{int(tutar)}</DisplayAmount>
    <CurrencyCode>{str('0949')}</CurrencyCode>
    <MerchantOrderId>{str(merchant_order_id)}</MerchantOrderId>
    <TransactionSecurity>{int('3')}</TransactionSecurity>
    </KuveytTurkVPosMessage>
    """
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(SANAL_POS['kart_onay_url'], data=data.encode('ISO-8859-9'), headers=headers)
    if r.status_code == 200:
        user_package = UserPackage.objects.create(user=request.user, package=package, unlocked=True)
        purchased_videos = Video.objects.filter(package=package)
        purchase = Purchase.objects.create(user=request.user, package=package, successful=True)
        purchase.videos.set(purchased_videos)
        return HttpResponse(r)
    else:
        user_package = UserPackage.objects.create(user=request.user, package=package, unlocked=False)
        user_package.delete()
        return render(request, 'payment_failure.html')  

    context = {
        'package': package,
        'user_package': user_package,
    }

    return render(request, 'odeme.html', context)




@require_http_methods(['POST'])
@csrf_exempt
def ok_url(request):
      

    gelen = request.POST.get('AuthenticationResponse')
    data = urllib.parse.unquote(gelen)
    merchant_order_id_start = data.find('<MerchantOrderId>')
    merchant_order_id_stop = data.find('</MerchantOrderId>')
    merchant_order_id = data[merchant_order_id_start + 17:merchant_order_id_stop]
    amount_start = data.find('<Amount>')
    amount_end = data.find('</Amount>')
    amount = data[amount_start + 8:amount_end]
    md_start = data.find('<MD>')
    md_end = data.find('</MD>')
    md = data[md_start + 4:md_end]
    hashed_password = base64.b64encode(
        hashlib.sha1(SANAL_POS["password"].encode('ISO-8859-9')).digest()).decode()
    hashed_data = base64.b64encode(hashlib.sha1(
        f'{SANAL_POS["merchant_id"]}{merchant_order_id}{amount}{SANAL_POS["username"]}{hashed_password}'.encode(
            "ISO-8859-9")).digest()).decode()
    xml = f"""
    <KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <APIVersion>1.0.0</APIVersion>
    <HashData>{hashed_data}</HashData>
    <MerchantId>{int(SANAL_POS['merchant_id'])}</MerchantId>
    <CustomerId>{int(SANAL_POS['customer_id'])}</CustomerId>
    <UserName>{str(SANAL_POS['username'])}</UserName>
    <TransactionType>Sale</TransactionType>
    <InstallmentCount>0</InstallmentCount>
    <Amount>{amount}</Amount>
    <MerchantOrderId>{str(merchant_order_id)}</MerchantOrderId>
    <TransactionSecurity>3</TransactionSecurity>
    <KuveytTurkVPosAdditionalData>
    <AdditionalData>
    <Key>MD</Key>
    <Data>{md}</Data>
    </AdditionalData>
     </KuveytTurkVPosAdditionalData>
    </KuveytTurkVPosMessage>
    """
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(SANAL_POS['odeme_onay_url'], data=xml.encode('ISO-8859-9'), headers=headers)
    return HttpResponse(r)


@require_http_methods(['POST'])
@csrf_exempt
@login_required
def fail_url(request):
    user_package = UserPackage.objects.filter(user=request.user)
    user_package.delete()

    context = {
        'message': 'Payment failed. Your packages have been removed.',
    }
    template = 'main/fail-url.html'
    response_content = render(request, template, context).content

    response = HttpResponse(response_content, content_type='text/html', status=400)
    return response
