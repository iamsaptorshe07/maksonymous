from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from django.views import View
from django.core.mail import send_mail
from django.urls import reverse
from accounts import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from allauth import socialaccount, account


def login_(request):

    email = request.POST['email_id']
    password = request.POST['password']
    user = models.User.objects.get(email=email)
    print(email)
    if check_password(password, user.password):
        return render(request, 'accounts/a.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    else:
        email = request.POST.get('email')
        password_f = request.POST.get('password')
        password_c = request.POST.get('cpassword')
        try:
            users = models.User.objects.get(email=email)

        except:
            users = False
        if users:
            x = 'Email Address Already Exists'
            return render(request, 'accounts/login.html', {'messag': x})
        if password_c != password_f:
            x = 'Password Doesnot Match'
            return render(request, 'accounts/login.html', {'messag': x})
        else:
            user = models.User.objects.create_user(
                email=email, password=password_c)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                           'uidb64': uidb64, 'token': token_generator.make_token(user)})

            activate_url = 'Http://' + domain + link
            subject = 'Activation Link'
            body = 'Hey, You are just ready to start enjoying Anonymous Messaging App. Just click on the link to activate your Account  ' + activate_url
            send_mail(subject, body, 'abhinav22agrawal@gmail.com',
                      [email], fail_silently=False, )
            print(activate_url, '+++++++++++++++++++++++++++++++++++++++++++++++++++')
            me = "We Have send an activation Link on " + email + \
                'Please Click on the link to activate account'
            return HttpResponse(me)


class Verification(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.User.objects.get(pk=uid)
        except:
            user = None
        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')


def a(request):
    data = socialaccount.models.SocialAccount.objects.get(
        user=request.user).extra_data
    email = data.get('email')
    print(email)
    return render(request, 'accounts/a.html')
