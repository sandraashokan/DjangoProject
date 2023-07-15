from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart,account,order
from shop.models import product


# Create your views here.
@login_required
def cart_view(request):
    total=0
    try:
        user=request.user
        cart=Cart.objects.filter(user=user)
        for i in cart:
            total+=i.quantity*i.products.price
    except Cart.DoesNotExist:
        pass
    return render(request,'cart.html',{'cart':cart,'total':total})
@login_required
def add_cart(request,p):
    products=product.objects.get(id=p)
    user=request.user
    try:
        cart=Cart.objects.get(products=products,user=user)
        if cart.quantity < cart.products.stock:
            cart.quantity+=1
        cart.save()
    except Cart.DoesNotExist:
        cart=Cart.objects.create(products=products,user=user,quantity=1)
        cart.save()
    return redirect('cart:cart_view')

@login_required
def cart_remove(request,p):
    user=request.user
    products=product.objects.get(id=p)
    try:
        cart=Cart.objects.get(user=user,products=products)
        if cart.quantity >1:
            cart.quantity -=1
            cart.save()

        else:
            cart.delete()

    except:


        pass
    return redirect('cart:cart_view')

@login_required
def full_remove(request,p):
    user=request.user
    products=product.objects.get(id=p)
    try:
        cart=Cart.objects.get(user=user,products=products)
        cart.delete()

    except:
        pass

    return redirect('cart:cart_view')

@login_required
def Order(request):
    total=0
    items=0
    msg=0
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        an=request.POST['an']
        user=request.user
        cart=Cart.objects.filter(user=user)
        for i in cart:
            total+=i.quantity*i.products.price
            items+=i.quantity
        a=account.objects.get(acnum=an)
        if float(a.amount) >= total:
              a.amount=a.amount-total
              a.save()
              for i in cart:
                  o=order.objects.create(user=user,products=i.products,address=a,phone=p,order_status="paid",noofitems=i.quantity)
              cart.delete()
              msg="Order Placed Successfully"
              return render(request,'orderdetail.html',{'msg':msg,'total':total,'items':items})
        else:
            msg="Insufficient Amount.You cant place order"
            return render(request,'orderdetail.html',{'msg':msg})


    return render(request,'placeorder.html')

@login_required
def orderview(request):
    user=request.user
    ord=order.objects.filter(user=request.user,order_status="paid")
    return render(request,"orderview.html",{'o':ord,'name':user.username})

