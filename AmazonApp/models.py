from typing import ChainMap
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    user_type_choices=((1,"Admin"),(2,"Staff"),(3,"Merchant"),(4,"Customer"))
    user_type=models.CharField(max_length=255,choices=user_type_choices,default=1)
 
class AdminUser(models.Model):
    profile_pic = models.FileField(default ="")
    auth_user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class StaffUser(models.Model):
    profile_pic =models.FileField(default = "")
    auth_user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantUser(models.Model):
    profile_pic =models.FileField(default = "")
    auth_user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    company_name =models.CharField(max_length=255)
    gst_details = models.CharField(max_length=255)
    address =models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerUser(models.Model):
    profile_pic = models.FileField(default='')
    auth_user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Subcategories(models.Model):
    id = models.AutoField(primary_key=True)
    category_id=models.ForeignKey(Categories,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    url_slug = models.CharField(max_length=255)
    Subcategories_id = models.ForeignKey(Subcategories,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_max_price = models.CharField(max_length=255)
    product_description = models.TextField()
    product_long_description=models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    added_by_merchant = models.ForeignKey(MerchantUser,on_delete=models.CASCADE)
    in_stock_total = models.IntegerField(default=1)
    is_active=models.IntegerField(default=1)

class ProductMedia(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type = models.CharField(max_length=255)
    media_content = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type_choices = ((1,"BUY"),(2,"SELL"))
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    transaction_product_count=models.IntegerField(default=1)
    transaction_type = models.CharField(choices=transaction_type_choices,max_length=255)
    transaction_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductDetails(models):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    title_details=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductAbout(models):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductTags(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviews(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    review_image = models.FileField()
    rating = models.CharField(default='5')
    reviews = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviewVoting(models.Model):
    id = models.AutoField(primary_key=True)
    product_review_id = models.ForeignKey(ProductReviews,on_delete=models.CASCADE)
    user_id_voting= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductVarient(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
   
class ProductVarientItems(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerOrders(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products,on_delete=models.DO_NOTHING)
    purchase_price = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    product_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderDeliveryStatus(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(CustomerOrders,on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

 

    







 