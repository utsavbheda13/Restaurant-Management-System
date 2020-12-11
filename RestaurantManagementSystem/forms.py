from django.forms import ModelForm
from RestaurantManagementSystem.models import Fooditems_Details,Customer_Information,Employee_Details

class Fooditems_DetailsForm(ModelForm):
    class Meta:
        model = Fooditems_Details
        fields = '__all__'
        labels ={
            'category_id' : 'Category',
        }

    def __init__(self,*args,**kwargs):
        super(Fooditems_DetailsForm,self).__init__(*args,**kwargs)
        self.fields['category_id'].empty_label = "Select Category"

class Customer_InformationForm(ModelForm):
    class Meta:
        model = Customer_Information
        fields = ('customer_name','customer_total','customer_address','customer_city','customer_state','customer_pincode','customer_emailid','customer_mobileno')
        labels = {
            'customer_name' : 'Name:',
            'customer_total' : 'Number Of Persons:',
            'customer_address' : 'Address:',
            'customer_city' : 'City:',
            'customer_state' : 'State:',
            'customer_pincode' : 'Pin Code:',
            'customer_emailid' : 'Email:',
            'customer_mobileno' : 'Mobile No.:',
        }

class Employee_DetailsForm(ModelForm):
    class Meta:
        model = Employee_Details
        fields='__all__'
