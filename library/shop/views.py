from django.shortcuts import render
from shop.models import category,product
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

def allproductcat(request):
    c=category.objects.all()
    return render(request,'category.html',{'c':c})

def allproducts(request,cslug):
    c=category.objects.get(slug=cslug)
    p=product.objects.filter(category__slug=cslug)
    return render(request,'products.html',{'p':p,'c':c})

def prodetail(request,pslug):
    p=product.objects.get(slug=pslug)
    return render(request,'detail.html',{'p':p})

def user_login(request):
    if (request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u, password=p)
        if user:
            login(request,user)
            return allproductcat(request)
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return allproductcat(request)

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        n=request.POST['n']
        l=request.POST['l']
        e=request.POST['e']
        p=request.POST['p']
        cp=request.POST['cp']
        if p==cp:
           user=User.objects.create_user(username=u,first_name=n, last_name=l, email=e, password=p,)
           user.save()
           return user_login(request)
    return render(request,'register.html')


