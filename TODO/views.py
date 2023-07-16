from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from TODO.form import TODOForm
from TODO.models import TODO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user=request.user
        form=TODOForm()
        todos=TODO.objects.filter(user=user).order_by('priority')
    return render(request,'index.html',context={'form':form,'todos':todos})
def loginview(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        passlo=request.POST.get('password')
        user=authenticate(request,username=username,password=passlo)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("user password incorrect!!!!")
    return render(request,'login.html')

def signupview(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        repass1 = request.POST.get('repassword')
        if pass1!=repass1:
            return HttpResponse("Password And Repassword are not Same")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')
def logoutpage(request):
    logout(request)
    return redirect('login')
def add_todo(request):
    if request.user.is_authenticated:
        user=request.user
        form=TODOForm(request.POST)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.user=user
            todo.save()
            return redirect('home')
        else:
            return render(request, 'index.html', context={'form':form})
    else:
       return redirect("home")
def delete_todo(request,id):
    TODO.objects.get(pk=id).delete()
    return redirect('home')
def change_todo(request , id , status):
    todo = TODO.objects.get(pk = id)
    todo.status=status
    todo.save()
    return redirect('home')
# Create your views here

