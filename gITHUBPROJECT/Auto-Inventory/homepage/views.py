from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill
from django.contrib import messages
from django.utils.http import urlencode
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse
from homepage.functions.send_mail import send_registration_link
from homepage.functions.generate_verification import generate_verification_token
from .models import UserProfile

class HomeView(View):
    template_name = "home.html"
    def get(self, request):       
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases,
        }
        return render(request, self.template_name, context)

class AboutView(TemplateView):
    template_name = "about.html"

class UnderWorkView(TemplateView):
    template_name = "working.html"

class RegisterView(TemplateView):
    template_name = "register.html"

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if UserProfile.objects.filter(username=username, verification_status=True).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
        elif UserProfile.objects.filter(useremail=email, verification_status=True).exists():
            messages.error(request, 'Email address already exists. Please choose another one.')
        else:
            verification_token = generate_verification_token()
            registration_link = f"http://127.0.0.1:8000/verify-email/?username={username}&verification-token={verification_token}"
            print(verification_token)
            send_registration_link(username, email, registration_link)
            if UserProfile.objects.filter(useremail=email).exists():
                user_profile = UserProfile.objects.get(useremail=email)
                user_profile.verification_token = verification_token
                user_profile.save()
            else:
                user_profile = UserProfile.objects.create_user(username=username, useremail=email, password=password, verification_token=verification_token)
            messages.success(request, 'Your account has been created successfully. Please verify your email!')
            login_url = f"{reverse('login')}?{urlencode({'next': '/'})}"
            return redirect(login_url)
    
    return render(request, 'register.html')

def email_verification(request):
    username = request.GET.get('username')
    verification_token = request.GET.get('verification-token')
    user_profile = UserProfile.objects.filter(username=username, verification_token=verification_token).first()
    
    if user_profile is not None:
        user_profile.verification_status = True
        user_profile.save()
        return render(request, 'verified.html')
    else:
        return render(request, 'verification_failed.html')

class LoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_email_verified():
            messages.success(self.request, "This account has not been verified.")
            return redirect('login')  
        return super().form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        login_url = f"{reverse('login')}?{urlencode({'next': '/'})}"
        return redirect(login_url)