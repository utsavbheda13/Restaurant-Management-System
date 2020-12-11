from django.db import models

class Category_Details(models.Model):
    category_id=models.IntegerField(primary_key=True)
    category_description=models.CharField(max_length=20)
    def __str__(self):
        return self.category_description

class Fooditems_Details(models.Model):
    fooditem_id=models.IntegerField(primary_key=True,auto_created=True)
    fooditem_name=models.CharField(max_length=30)
    fooditem_description=models.TextField(max_length=300)
    fooditem_price=models.FloatField(max_length=6)
    category_id=models.ForeignKey('Category_Details',on_delete=models.CASCADE)
    fooditem_photo=models.ImageField(upload_to='items',null=True)
    def __str__(self):
        return self.fooditem_name

# class Items_Master(models.Model):
#     item_id=models.IntegerField(primary_key=True)
#     item_name=models.CharField(max_length=30)

# class Fooditems_Items(models.Model):

class Customer_Information(models.Model):
    customer_id=models.IntegerField(primary_key=True,auto_created=True)
    customer_name=models.CharField(max_length=20)
    customer_total=models.IntegerField()
    customer_address=models.TextField(max_length=200)
    customer_city=models.CharField(max_length=20)
    customer_state=models.CharField(max_length=20,null=True)
    customer_pincode=models.IntegerField()
    customer_mobileno=models.IntegerField()
    customer_emailid=models.CharField(max_length=25)
    table_id=models.IntegerField(default=0)
    def __str__(self):
        return self.customer_name

class Employee_Details(models.Model):
    emp_id=models.IntegerField(primary_key=True)
    emp_name=models.CharField(max_length=20)
    emp_address=models.TextField(max_length=200)
    emp_city=models.CharField(max_length=20)
    emp_state=models.CharField(max_length=20)
    emp_pincode=models.IntegerField()
    emp_mobileno=models.IntegerField()
    emp_emailid=models.CharField(max_length=25)
    def __str__(self):
        return self.emp_name

class Table_Master(models.Model):
    table_id=models.IntegerField(primary_key=True,auto_created=True)
    table_capacity=models.IntegerField()
    # emp_id=models.ForeignKey('Employee_Details',on_delete=models.CASCADE)
    # customer_id=models.ForeignKey('Customer_Information',on_delete=models.CASCADE)
    table_occupied=models.BooleanField()
    # def __str__(self):
    #     return self.table_id

class Order_Details(models.Model):
    order_id=models.IntegerField(primary_key=True,auto_created=True)
    order_date=models.DateTimeField('date published')
    # table_id=models.ForeignKey('Customer_Information',on_delete=models.CASCADE)
    # emp_id=models.ForeignKey('Employee_Details',on_delete=models.CASCADE)
    fooditem_id=models.ForeignKey('Fooditems_Details',on_delete=models.CASCADE)
    quantity=models.IntegerField()
    fooditem_price=models.FloatField()
    amount=models.FloatField()
    # def __str__(self):
    #     # order_id=str(order_id)
    #     return self.order_id

# class Order_Items(models.Model):
#     orderitem_id=models.IntegerField(primary_key=True,auto_created=True)
#     order_id=models.ForeignKey('Order_Details',on_delete=models.CASCADE)
#     # fooditem_id=models.ForeignKey('Fooditems_Details',on_delete=models.CASCADE)
#     quantity=models.IntegerField()
#     fooditem_price=models.FloatField()
#     amount=models.FloatField()

class Salesbill(models.Model):
    salesbill_no=models.IntegerField(primary_key=True)
    salesbill_date=models.DateTimeField('date published')
    order_id=models.ForeignKey('Order_Details',on_delete=models.CASCADE)
    customer_id=models.ForeignKey('Customer_Information',on_delete=models.CASCADE)
    order_amount=models.FloatField()
    tax=models.FloatField()
    discount=models.FloatField()
    net_amount=models.FloatField()

