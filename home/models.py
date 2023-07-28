from django.db import models

# Create your models here.
class product(models.Model):
    class Meta:
        db_table = 'product' # Để django hiểu tìm bảng product

    id = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=512, default='')
    name = models.CharField(max_length=255, default='')
    price = models.IntegerField(default='0')
    sale_price = models.IntegerField(default='0')
    amount = models.IntegerField(default='0')
    desc = models.CharField(max_length=512, default='')
    reviews = models.IntegerField(default='0')
    quantity_sold = models.IntegerField(default='0')
    display = models.BooleanField(default='1')
    

class account(models.Model):
    class Meta:
        db_table = 'account'
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)