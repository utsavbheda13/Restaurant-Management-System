from django.contrib import admin

# Register your models here.
from .models import Category_Details,Fooditems_Details,Customer_Information,Employee_Details,Table_Master,Order_Details,Salesbill

admin.site.register(Category_Details)
admin.site.register(Fooditems_Details)
# admin.site.register(Items_Master)
admin.site.register(Customer_Information)
admin.site.register(Employee_Details)
admin.site.register(Table_Master)
admin.site.register(Order_Details)
# admin.site.register(Order_Items)
admin.site.register(Salesbill)