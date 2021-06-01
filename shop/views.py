from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password,check_password
from shop.models import Product
from shop.models import Category
from shop.models import User
from shop.models import Cart
from shop.models import CartProduct
# Create your views here.
# password hashing to change the password into somecode uses method makepassword for decoading uses check_password
def base(request):
    products=None
    #if not none it will give error products before assignment
    #request.session.clear()
    categories=Category.get_all_categories()#get all objects in categories by declaring method in models.py
    categoryID=request.GET.get('category')# users/?categort url in home.html for getting query sets.Query set if user passes request for categories user req stored in catergoryId
    if categoryID:
      products=Product.get_all_product_by_id(categoryID)#product to gets products of that categories
    else:
        products = Product.get_all_products()
      #we want pass two disc key so here is empty disc
    data= {}
    data['products']=products#key:value
    data['categories']=categories
    return render(request,'home.html',data)
  
def signup(request):
  if request.method =="GET":
    return render(request,'signup.html')
  else:
      fullname=request.POST.get('fullname')
      email=request.POST.get('email')
      password=request.POST.get('password')
      passwordagain=request.POST.get('passwordagain')
      phoneno=request.POST.get('phoneno')
      city=request.POST.get('city')
      #we can add required by directly used in signup.html or can add required here
      user=User(fullname=fullname,email=email,password=password,phoneno=phoneno,city=city)
      #value for showing in for after getting error msg it get vanished to prevent that uses value="{{value.fullname}}" so even after loading a page after erroer some values still remain same 
      value={
        'fullname':fullname,
        'phoneno':phoneno,
        'city':city,
        'email':email,
      }
      error_message=None
      if len(phoneno)!=10:
        error_message="Invalid Phonenumber!!!!!"
      elif password!=passwordagain:
        error_message="password doesnot match!!!!"
      elif user.isExist():
        error_message="Email already exist!!!"
  
      elif user.is_exist():
        error_message="Phone Number already exist!!!!"  

      if not error_message:  
        print(fullname,email)
        #user=User(fullname=fullname,email=email,password=password,phoneno=phoneno,city=city)#we are testing unique email so creating User object earlier then test then save
        user.password=make_password(user.password)
        user.save()
        message=None
        message="created account succesfully"
        #return HttpResponse(request.POST.get('name'))
        #return render(request,'signup.html',{'message':message})#for sucess msg
        return redirect('home')#redirect 
  
      else:
        data={
          'error':error_message,
          'value':value
        }
    
        return render(request,'signup.html',data)

def login(request):
  if request.method == 'GET':
    return render(request,'login.html')
  else:
      email=request.POST.get('email')
      password=request.POST.get('password')
      user=User.get_customer_email(email)
      error_message=None
      if user:
         flag =check_password(password,user.password)
         if flag:
          request.session['user']=user.id
          #request.session['email']=user.email
          return redirect('home')
         else:
           error_message="Invalid Username or Password!!!"
           return render(request,'login.html',{'error':error_message})

      else:
        error_message="Invalid Username or Password!!!"  
        return render(request,'login.html',{'error':error_message})

def viewdata(request,id):
  #feching product by Id
  products=Product.objects.filter(id=id)
  return render(request,'view.html',{'products':products})

def searchdata(request):
  #icontains for searching data we have to use"__"after variable passing 
  #No result found then passing search as query and using {{empty }}block for no results
  #if no query and press search button it will show all products as we uses our homepage html file then copy tha
  search=request.GET['search']
  products=Product.objects.filter(name__icontains=search)
  
  data={'products':products,'search':search}

  return render(request,'search.html',data)

def logout(request):
  request.session.clear()

  return redirect(login)

#def addtocart(request,id):
 # products=Product.objects.filter(id=id)
#  return render(request,'addtocart.html',{'products':products})

class AddtocartView(TemplateView):
  template_name="addtocart.html"

  def  get_context_data(self,**kwargs):
    context=super().get_context_data(**kwargs)
    #get product id from requested url
    product_id=self.kwargs['id']# getting id grom url of add to cart
    print(product_id)#product id ex 1
    #get product #get method returns matching object
    pro_obj=Product.objects.get(id=product_id)
    #check if cart exist
    cart_id=self.request.session.get("cart_id",None)
    if cart_id:
      cart_obj=Cart.objects.get(id=cart_id)#getting  cart id in cart_obj
      print("old cart")
      #if product we added exist
      this_product_in_cart=cart_obj.cartproduct_set.filter(product=pro_obj)#cart_objobject of cart then "related object reference" uses on foreignkey items.cartproduct_set(CartProduct is model )then can use any method in cartproduct model there is product field we are mathing our product from request to data of product in model neccesarly need cart obj for cartproduct_set cartproduct uses as related object refernce

      if this_product_in_cart.exists():
        cartproduct=this_product_in_cart.last()#last() for getting last object
        cartproduct.quantity+=1#cartproduct referce used to get quantity field from cartproduct model
        cartproduct.subtotal+=pro_obj.price
        cartproduct.save()
        cart_obj.total+=pro_obj.price
        cart_obj.save()

      else:#if product we added doesnot exist in cart
      #have to create objects forfiled exist in cartproduct model explicitly
        cartproduct=CartProduct.objects.create(cart=cart_obj,product=pro_obj,rate=pro_obj.price,quantity=1,      subtotal=pro_obj.price)
        #quantity is 1 becz first time added only 1 product there hence subtotal is equal to price
        cart_obj.total+=pro_obj.price#incresing cart value
        cart_obj.save()


    else:
      cart_obj=Cart.objects.create(total=0)
      #we created the cart and save in session for next time
      self.request.session['cart_id']=cart_obj.id#created id in cart_obj then get id and assing to cart_id
      print("new cart")
      #creating cart as well getting product information
      cartproduct=CartProduct.objects.create(cart=cart_obj,product=pro_obj,rate=pro_obj.price,quantity=1,      subtotal=pro_obj.price)
        #quantity is 1 becz first time added only 1 product there hence subtotal is equal to price
      cart_obj.total+=pro_obj.price#incresing cart value
      cart_obj.save()

    #check if product already exist in cart

    return context


def cart(request):
     cartobj=CartProduct.objects.all()
     cart_id=request.session.get("cart_id",None)
     if cart_id:
         cart=Cart.objects.get(id=cart_id)
     else:
         cart=None
        
     context={'cartobj':cartobj,'cart':cart}

     return render(request,'cart.html',context)





def managecart(request,cp_id):
    action=request.GET.get("action")
    
    cp_obj=CartProduct.objects.get(id=cp_id)
    cart_obj= cp_obj.cart
    print(cp_id,action)
    if action=="inc":
     cp_obj.quantity+=1
     cp_obj.subtotal+=cp_obj.rate
     cp_obj.save()
     cart_obj.total+=cp_obj.rate
     cart_obj.save()

    elif action=="dcr":
     cp_obj.quantity-=1
     cp_obj.subtotal-=cp_obj.rate
     cp_obj.save()
     cart_obj.total-=cp_obj.rate
     cart_obj.save()
     if cp_obj.quantity==0:
       cp_obj.delete()
      
    elif action=="rmv"  :
      cart_obj.total-=cp_obj.subtotal
      cart_obj.save()
      cp_obj.delete()

    else:
      pass

    return redirect('cart')


def emptycart(request):
  
     cart_id=request.session.get("cart_id",None)
     if cart_id:
         cart=Cart.objects.get(id=cart_id)
         cartobj=cart.cartproduct_set.all().delete()
         cart.total=0
         cart.save()
     return redirect('cart')

def shippinginfo(request):
    cartobj=CartProduct.objects.all()
    cart_id=request.session.get("cart_id",None)
    if cart_id:
         cart=Cart.objects.get(id=cart_id)
    else:
         cart=None
    data={'cartobj':cartobj,'cart':cart}
    return render(request,'shippingform.html',data)

