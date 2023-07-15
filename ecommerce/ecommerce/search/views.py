from django.shortcuts import render
from shop.models import product
from django.db.models import Q
# Create your views here.
def searchresult(request):
    products=None
    query=""
    if request.method=="POST":
        query=request.POST.get('s')
        if query:
            products=product.objects.filter(Q(name_icontains=query) | Q(description_icontain=query))
    return render(request,'search.html',{'query':query,'products':products})