from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from shop.models import product


# Create your views here.
@login_required
def cart_view(request):
    try:
        user=request.user
        cart=Cart.objects.filter(user=user)
    except Cart.DoesNotExist:
        pass
    return render(request,'cart.html',{'cart':cart})
@login_required()
def add_cart(request,p):
    products=product.objects.get(id=p)
    user=request.user
    cart=Cart.objects.create(products=products,user=user,quantity=1)
    cart.save()
    return render(request,'cart.html')