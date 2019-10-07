
from django.shortcuts import render,redirect
from . import models
from .forms import UserForm,RegisterForm
import hashlib
import requests


def index(request):
    ctx={}
    if request.POST:
        ctx['rlt']=request.POST['q']
        get_vars={'key':'14867e0f81fd4a93b9f709f780cffc2c','domainName':request.POST['q']}
        get_url="http://apidata.chinaz.com/CallAPI/Domain"
        r=requests.get(get_url,params=get_vars).text
        ctx['rlt']=r
    return render(request,'login/index.html',ctx)

def login(request):
    if request.method=="POST":
        login_form=UserForm(request.POST)
        message="请检查填写的内容！"
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            try:
                user=models.User.objects.get(name=username)
                if user.password==password:
                    request.session['is_login']=True
                    request.session['user_id']=user.id
                    request.session['user_name']=user.name
                    return redirect('/index/')
                else:
                    message="密码不正确！"
            except:
                message="用户名不存在！"
        return render(request,'login/login.html',locals())
    login_form=UserForm
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method=="POST":
        register_form=RegisterForm(request.POST)
        message="请检查填写的内容！"
        if register_form.is_valid():
            username=register_form.cleaned_data['username']
            password1=register_form.cleaned_data['password1']
            password2=register_form.cleaned_data['password2']
            email=register_form.cleaned_data['email']
            sex=register_form.cleaned_data['sex']
            if password1 != password2:
                message="两次输入的密码不同！"
                return render(request,'login/register.html',locals())
            else:
                same_name_user=models.User.objects.filter(name=username)
                if same_name_user:
                    message='用户已经存在，请重新选择用户名！'
                    return render(request,'login/register.html',locals())
                same_email_user=models.User.objects.filter(email=email)
                if same_email_user:
                    message='该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request,'login/register.html',locals())
                new_user=models.User.objects.create()
                new_user.name=username
                new_user.password=password1
                new_user.email=email
                new_user.sex=sex
                new_user.save()
                return redirect('/login/')
    register_form=RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')

def hash_code(s,salt='mysite_login'):
    h=hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def wx(request):
    ctx={}
    if request.POST:
        ctx['rlt']=request.POST['q']
        get_vars = {'url': request.POST['q']}
        r = requests.get("https://tgops0.com/tools/checkWx", params=get_vars)
        ctx['rlt'] = r.text
    return render(request,'login/wx.html',ctx)

def qq(request):
    ctx={}
    if request.POST:
        ctx['rlt']=request.POST['q']
        get_vars = {'url': request.POST['q']}
        r = requests.get("https://tgops0.com/tools/checkQQ", params=get_vars)
        ctx['rlt'] = r.text
    return render(request,'login/qq.html',ctx)
