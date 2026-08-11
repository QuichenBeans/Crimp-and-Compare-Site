from django.contrib import admin
from .models import Shoe, Category, RetailerOffer, AwinProduct, Dictionary, Guide

# Register your models here.

admin.site.register(Shoe)
admin.site.register(Category)
admin.site.register(RetailerOffer)
admin.site.register(AwinProduct)
admin.site.register(Guide)
admin.site.register(Dictionary)