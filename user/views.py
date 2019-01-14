from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from user.forms import UserLoginForm,UserRegisterForm
import re
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from user.forms import UserProForm
from user.models import UserPro
from django.views.generic.edit import View




# Create your views here.
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect("blog:blog")
            else:
                return render(request,'user/login.html',{'errmsg':"用户名或密码输入有误，请重新输入",
                                                         'username':username,
                                                         'password':password})
    elif request.method == 'GET':
        return render(request,'user/login.html',{'errmsg':None})

def user_logout(request):
    logout(request)
    return redirect("blog:blog")

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=user_register_form.cleaned_data['username'],password=user_register_form.cleaned_data['password'])
            login(request,user)
            return redirect("blog:blog")
        else:
            return render(request, 'user/register.html', {'username':username,
                                                          'email':email,
                                                          'password':password,
                                                          'password2':password2,
                                                          'errmsg': user_register_form.errors['__all__'][0]})
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        return render(request,'user/register.html',{'user_register_form':user_register_form,
                                                    'errmsg':None})

@login_required(login_url='user/login')
def user_delete(request,user_id):
    user = User.objects.get(id=user_id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect('blog:blog')

@login_required(login_url='user/login')
def user_edit(request,user_id):
    user = User.objects.get(id=user_id)
    userpro = UserPro.objects.get(user_id=user_id)
    if request.method == 'POST':
        if request.user != user:
            return render(request,'user/edit.html',{'userpro':userpro,
                                                    'errmsg':'您没有权限修改该用户信息！'})
        userpro_form = UserProForm(request.POST,request.FILES)
        if userpro_form.is_valid():
            userpro.phone = request.POST['phone']
            userpro.bio = request.POST['bio']
            if 'avatar' in request.FILES:
                userpro.avatar = request.FILES['avatar']
            userpro.save()
            return redirect('blog:blog_list')
    elif request.method == 'GET':
        userpro_form = UserProForm()
        return render(request, 'user/edit.html', {'userpro_form':userpro_form,
                                                  'userpro':userpro,
                                                  'user':user,
                                                  'errmsg':None})


