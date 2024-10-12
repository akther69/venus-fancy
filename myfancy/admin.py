from django.contrib import admin

# Register your models here.

from myfancy.models import Material,Occasion,Colour,Feature,Type,Tag,Size,Product,ProductVariant,Orders

admin.site.register(Material)

admin.site.register(Occasion)

admin.site.register(Colour)

admin.site.register(Feature)

admin.site.register(Type)

admin.site.register(Tag)

admin.site.register(Size)

admin.site.register(Product)

admin.site.register(ProductVariant)

admin.site.register(Orders)