from django.contrib import admin

from pizza.models import Pizza, Extra, Ingredient, Order

admin.site.register(Pizza)
admin.site.register(Extra)
admin.site.register(Order)
admin.site.register(Ingredient)
