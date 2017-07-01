from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quote
from django.db.models import Count, Sum

def index(request):
    return render(request,"login_app/index.html")

def add(request):
    if request.method == 'POST':
        answer = User.objects.makeUser(request.POST['name'],request.POST['alias'],request.POST['email'],request.POST['password'],request.POST['confirmpassword'])
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
        print('success')
        return redirect('/success')
    else:
        messages.info(request, "Invalid email or password")
        print('error')
        return redirect('/')

def success(request):
    if 'userId' in request.session:
        context ={
            "pull" : User.objects.get(id=request.session['userId']),
            "quotes" : Quote.objects.all()
            }
    return render(request, "login_app/success.html", context)


def process(request):
    quoter = User.objects.get(id=request.session['userId'])
    if request.method == 'POST':
        Quote.objects.makeQuote(quoter,request.POST['quotedby'],request.POST['message'])

    elif len(Quote.objects.filter(quoter=quoter)) > 0:
        numQuotes = Quote.objects.get(quoter=quoter)
        numQuotes.counter = int(numQuotes.counter) + 1
        numQuotes.save()
    else:
        quote = Quote()
        quote.quoter = quoter
        quote.counter = 1
        quote.save()

    return redirect('/success')

def logout(request):
    del request.session['userId']
    return redirect('/')

def users(request, userId):
    if 'userId' in request.session:
        context ={
            "pull" : User.objects.get(id=userId),
            "quotes" : Quote.objects.filter(quoter=userId),
            }
    return render(request,"login_app/users.html", context)
