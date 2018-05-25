from django.conf.urls import url

from .views import (
    cart_home,
    cart_update,
    )

urlpatterns = [
    url(r'^cart_update/$', cart_update, name='update'),
    url(r'^$', cart_home, name='home'),

]
