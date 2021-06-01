from django.contrib import admin
from shop.models import Category
from shop.models import Product
from shop.models import User
from shop.models import Cart
from shop.models import CartProduct

# Register your models here.


class AdminCategory(admin.ModelAdmin):
    list_display=['name']

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category']

class AdminUser(admin.ModelAdmin):
    list_display=['fullname','email','phoneno','password','passwordagain','city'] 

class AdminCart(admin.ModelAdmin):   
    list_display=['total'] 

class AdminCartProduct(admin.ModelAdmin):
    list_display=['cart','product','rate','quantity','subtotal']     

admin.site.register(User,AdminUser)
admin.site.register(Category,AdminCategory)
admin.site.register(Product,AdminProduct)
admin.site.register(Cart,AdminCart)
admin.site.register(CartProduct,AdminCartProduct)