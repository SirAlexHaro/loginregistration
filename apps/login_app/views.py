from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request,"login_app/index.html")

def add(request):
    if request.method == 'POST':
        answer = User.objects.makeUser(request.POST['firstname'],request.POST['lastname'],request.POST['email'],request.POST['password'],request.POST['confirmpassword'])
        if answer['status']:
            request.session['userId'] = answer['user'].id
            return redirect ('/success')
        else:
            for errors in answer['user']:
                messages.add_message(request, messages.ERROR, "registration {}".format(errors))
            return redirect('/')

def login(request):
    print "post:", request.POST
    answer = User.objects.log(request.POST['email'],request.POST['password'])
    print answer
    if answer['status']:
        request.session['userId'] = answer['user'].id
        return redirect ('/success')
    else:
        messages.info(request, "Invalid email or password")
        return redirect ('/')

def success(request):
    context ={
    "pull" : User.objects.get(id=request.session['userId'])
    }
    return render(request, "login_app/success.html",context)
