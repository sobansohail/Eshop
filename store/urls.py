from .views import index , signup ,login,logout,cart,checkout,end
from django.urls import path


urlpatterns = [
    path('',index,name='homepage'),
    path('signup',signup,name='signup'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('cart',cart,name='cart'),
    path('checkout',checkout,name='checkout'),
    path('end',end,name='end')
]
