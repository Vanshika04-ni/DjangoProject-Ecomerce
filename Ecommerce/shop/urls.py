from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from shop import views

urlpatterns = [
    
    path('',views.base,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('view/<int:id>',views.viewdata,name="viewdata"),
    path('search/',views.searchdata,name='searchdata'),
    path('logout/',views.logout,name='logout'),
    path('addtocart/<int:id>',views.AddtocartView.as_view(),name='addtocart'),
    path('cart/',views.cart,name='cart'),
    path('shipping/',views.shippinginfo,name='shipping'),
    path('managecart/<int:cp_id>/',views.managecart,name='managecart'),
    path('empty/',views.emptycart,name='empty')
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)