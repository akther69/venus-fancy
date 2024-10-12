from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.db.models import Sum,F,Avg
# Create your models here.

class UserProfile(models.Model):
    
    pic=models.ImageField(upload_to="profile_pictures",default="/profile_pictures/default_profile_picture.jpeg")
    
    name=models.CharField(max_length=200,null=True)
    
    bio=models.CharField(max_length=200,null=True)
    
    phone=models.IntegerField(null=True)
    
    address=models.CharField(max_length=400,null=True)
    
    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.user_object.username
    
class Material(models.Model):
    
    name=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
class Occasion(models.Model):
    
    name=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
class Colour(models.Model):
    
    name=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
class Feature(models.Model):
    
    name=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
class Type(models.Model):
    
    name=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
class Tag(models.Model):
    
    title=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.title
    
class Size(models.Model):
    
    name=models.CharField(max_length=200,unique=True)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
class Product(models.Model):
    
    title=models.CharField(max_length=200)
    
    description=models.TextField()
    
    image=models.ImageField(upload_to="product_picture",default="/product_picture/default_product_picture.png")
    
    material_object=models.ManyToManyField(Material)
    
    occasion_object=models.ForeignKey(Occasion,on_delete=models.CASCADE)
    
    feature_object=models.ManyToManyField(Feature)
    
    type_object=models.ForeignKey(Type,on_delete=models.CASCADE)
    
    tag_object=models.ManyToManyField(Tag)
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="products")
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    @property
    
    def review_count(self):
        
        return self.product_reviews.all().count()
    
    @property
    def average_rating(self):
        
        avg_rating=self.product_reviews.all().values("rating").aggregate(avg=Avg("rating")).get("avg",0)
        
        if avg_rating is None:
            
            return 0
        
        return round(avg_rating,1)
    
    def __str__(self):
        
        return self.title
    
class ProductVariant(models.Model):
    
    product_object=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_variants")
    
    colour_object=models.ManyToManyField(Colour)
    
    size_object=models.ManyToManyField(Size)
    
    price=models.PositiveIntegerField()
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    @property
    def purchased_count(self):
        
        return Orders.objects.filter(is_paid=True,cart_items_object__product_variant_object=self).count()
    
    
class Cart(models.Model):
    
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    @property
    
    def cart_total(self):
        
        return self.basket_items.filter(is_order_placed=False).annotate(total_price=F('product_variant_object__price') * F('quantity')).aggregate(total=Sum('total_price')).get('total',0)
    

class Cart_items(models.Model):
    
    product_variant_object=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    
    size_object=models.ForeignKey(Size,on_delete=models.CASCADE)
    
    colour_object=models.ForeignKey(Colour,on_delete=models.CASCADE)
    
    cart_object=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="basket_items")
    
    quantity=models.PositiveIntegerField()
    
    is_order_placed=models.BooleanField(default=False)
    
    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    
    @property
    def item_total_price(self):
        
        return self.product_variant_object.price * self.quantity
    
    
class Address(models.Model):
    
    user_object = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name=models.CharField(max_length=200)
    
    phone = models.IntegerField()
    
    email = models.EmailField()
    
    pin = models.IntegerField()
    
    delivery_address = models.TextField()
    
    payment_options = (
        ("cash_on_delivery", "Cash On Delivery"),
        ("online_payment", "Online Payment")
    )
    
    payment_method = models.CharField(max_length=200, choices=payment_options, default="online_payment")
    
    created_date = models.DateTimeField(auto_now_add=True)
    
    updated_date = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)


class Orders(models.Model):
    cart_items_object = models.ManyToManyField(Cart_items)

    user_object = models.ForeignKey(User, on_delete=models.CASCADE)

    order_id = models.CharField(max_length=200, null=True)

    address_object = models.ForeignKey(Address, on_delete=models.CASCADE,related_name="address_detail")

    is_paid = models.BooleanField(default=False)
    
    is_canceled = models.BooleanField(default=False)
    
    canceled_at = models.DateTimeField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    total=models.FloatField(null=True)
   
    
from django.core.validators import MinValueValidator,MaxValueValidator

class Reviews(models.Model):
    
    product_object=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_reviews")
    
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)
    
    comment=models.TextField()
    
    rating=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    created_date = models.DateTimeField(auto_now_add=True)

    updated_date = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    
    class Meta:
        
        unique_together=('product_object','user_object')

    
    
def create_profile(sender,instance,created,*args, **kwargs):
    
    if created:
        
        UserProfile.objects.create(user_object=instance)
        
post_save.connect(receiver=create_profile,sender=User)     



def create_basket(sender,instance,created,*args, **kwargs):
    
    if created:
        
        Cart.objects.create(owner=instance)
        
post_save.connect(sender=User,receiver=create_basket)
    