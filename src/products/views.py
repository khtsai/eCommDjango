#from django.views import ListView
from django.http import Http404
from django.views.generic import ListView,DetailView
from django.shortcuts import render, get_object_or_404

from carts.models import Cart
from .models import Product
# Create your views here.

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"
    
    def get_context_data(self, *args,**kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    
    def get_object(self, queryset=None):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturn:
            qs = Product.objects.filter(slug=slug,active=True)
            instance = qs.first()
        except:
            raise Http404("Unknown...")
        
        return instance

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"
    
    def get_queryset(self):
        request = self.request
        return Product.objects.featured()
    
class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.featured()
    template_name = "products/featured-detail.html"
    
#     def get_queryset(self):
#         request = self.request
#         return Product.objects.featured()

class ProductListView(ListView):
    #queryset = Product.objects.all()
    template_name = "products/list.html"
    
#     def get_context_data(self,*args,**kwargs):
#         context = super(ProductListView, self).get_context_data(*args,*kwargs)
#         print(context)
#         return context
#         print output from above
#        {'paginator': None, 'page_obj': None, 'is_paginated': False, 
#        'object_list': <QuerySet [<Product: iPhone 8>, <Product: iPhone X>]>, 
#        'product_list': <QuerySet [<Product: iPhone 8>, <Product: iPhone X>]>, ....
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()
    
class ProductDetailView(DetailView):
    #queryset = Product.objects.all()
    template_name = "products/detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        print(context)
        return context
    
    def get_object(self, queryset=None):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist....")
        return instance
    
def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html",context)

def product_detail_view(request,pkk=None,*args,**kwargs):
    #instance = Product.objects.get(pk=pkk) #id
#     try:
#         instance = Product.objects.get(id=pkk)
#     except Product.DoesNotExist:
#         print("no product here")
#         raise Http404("Product doesn't exist")
#     except:
#         print("nothing...")

    qs = Product.objects.filter(id=pkk)
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exist.")
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         pkk = self.kwargs.get('pkk')
#         return Product.objects.filter(pk=pkk)     
    print(pkk)
    #instance = get_object_or_404(Product, pk=pkk)
    context = {
        'object': instance
    }
    return render(request, "products/detail.html",context)
