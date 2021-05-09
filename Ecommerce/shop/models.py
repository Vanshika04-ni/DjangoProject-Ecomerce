from django.db import models



class User(models.Model):
    fullname=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=200)
    passwordagain=models.CharField(max_length=200)
    phoneno=models.CharField(max_length=200)
    city=models.CharField(max_length=200)

    def isExist(self):
        if User.objects.filter(email=self.email):#for unique email 
            return True
        else:
            return False
    def is_exist(self):
        if User.objects.filter(phoneno=self.phoneno):#foe unique phonenumber
           return True
        else:
            return False  
    @staticmethod
    def get_customer_email(email):
        try:
          return User.objects.get(email=email)   
        except:
          return False



class Category(models.Model):
    name=models.CharField(max_length=200)

    def _str_(self):
        return self.name
    @staticmethod
    def get_all_categories():
        return Category.objects.all() 



class Product(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    price=models.FloatField()
    image=models.ImageField(null=True,blank=True)

 


    def _str_(self):
        return self.name

    @staticmethod
    def get_all_products():
        return Product.objects.all()    

    @property
    def imageURL(self):#for getting image url
        try:
            url=self.image.url
        except:
            url=''
        return url          
    @staticmethod
    def get_all_product_by_id(category_id):#filtering categories
        if category_id:
           return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    total=models.PositiveIntegerField(default=0)

    def __str__(self):
        return "cart:"+str(self.id)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField()

    def __str__(self):
        return "cart:"+str(self.cart.id) + "cartproduct:"+str(self.id)

class ShippingAddress(models.Model):
	userr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	cardproduct = models.ForeignKey(CartProduct, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)



	def _str_(self):
		return self.address
        