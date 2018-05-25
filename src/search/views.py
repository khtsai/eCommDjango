from django.shortcuts import render

from django.views.generic import ListView
from products.models import Product

# Create your views here.


class SearchProductView(ListView):
    template_name = "search/search_view.html"
    
    def get_context_data(self, *args,**kwargs):
        context = super(SearchProductView,self).get_context_data(*args,**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
        
    def get_queryset(self, *args, **kwargs):
        request = self.request
        dict_get = request.GET
        query = dict_get.get('q') # = dict_get['q']
        print(query)
        if query is not None:
            return Product.objects.search(query) # Product.objects.filter(query).distinct()
        return Product.objects.all()
    