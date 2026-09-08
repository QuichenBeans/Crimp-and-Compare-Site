from django.db import models
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default='shoes/default.jpg')
    slug = models.SlugField(unique=True)     
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify(self.name)
        super().save(*args, **kwargs)


class Shoe(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    fit_notes = models.TextField(max_length=1500)
    image_url = models.CharField(max_length=200, default='shoes/default.jpg')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.brand + ' - ' + self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify(self.name, self.brand)
        super().save(*args, **kwargs)


class RetailerOffer(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='offers')
    retailer = models.CharField(max_length=100)  # "BananaFingers", "Rock + Run"
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    affiliate_url = models.URLField()
    in_stock = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.retailer} - {self.shoe.brand} {self.shoe.name}"
    
    @property
    def discount_amount(self):
        return self.price - self.discounted_price
    

class AwinProduct(models.Model):
    product_name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3)
    awin_product_url = models.URLField(max_length=2000)
    awin_image_url = models.URLField(max_length=2000)
    merchant_name = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name + ' - ' + self.merchant_name

class Guide(models.Model):
    title = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(blank=True) # short description for a few lines in guide preview
    shoe = models.ManyToManyField(Shoe, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title + ' - ' + str(self.updated_date)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify(self.title)
        super().save(*args, **kwargs)

class Dictionary(models.Model):
    dictionary_heading_choices = [
        ('BALANCE AND BODY POSITION', 'Balance and Body Position'),
        ('FOOTWORK AND HANDHOLDS', 'Footwork and Handholds'),
        ('MOVEMENT AND TECHNIQUE', 'Movement and Technique'),
        ('ROUTE AND CLIMBING STYLE', 'Route and Climbing Style')
    ]
    heading = models.CharField(max_length=200, choices=dictionary_heading_choices) 
    term = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    example = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.term
    
    
        