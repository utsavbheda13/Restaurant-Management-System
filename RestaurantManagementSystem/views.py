from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from RestaurantManagementSystem.models import Table_Master,Customer_Information,Fooditems_Details,Order_Details,Employee_Details,Category_Details
from .forms import Fooditems_DetailsForm,Customer_InformationForm,Employee_DetailsForm
from datetime import datetime



def index(request):
    return render(request,'index.html')

def login(request):
    c={}
    c.update(csrf(request))
    return render(request,'login.html',c)

def auth_view(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user= auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/RestaurantManagementSystem/loggedin/')
    else:
        return HttpResponseRedirect('/RestaurantManagementSystem/invalidlogin/')

def forgotpass(request):
    return redirect('RestaurantManagementSystem/password_reset/')

@login_required(login_url='/RestaurantManagementSystem/login/')
def loggedin(request):
    return render(request,'AdminTemplate.html',{'full_name':request.user.username})

@login_required(login_url='/RestaurantManagementSystem/login/')
def invalidlogin(request):
    return render(request,'invalidlogin.html')

@login_required(login_url='/RestaurantManagementSystem/login/')
def logout(request):
    auth.logout(request)
    return render(request,'login.html')

def bookTable(request):
    if request.method == 'POST':
        form=Customer_InformationForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('/RestaurantManagementSystem/processtablerequest/')
    else:
        form=Customer_InformationForm()
    return render(request,'BookTable.html',{'form': form})

def processTableRequest(request):
    customer_name=request.POST.get('customer_name','')
    customer_address=request.POST.get('customer_address','')
    customer_city=request.POST.get('customer_city','')
    customer_state=request.POST.get('customer_state','')
    customer_pincode=request.POST.get('customer_pincode','')
    customer_emailid=request.POST.get('customer_emailid','')
    customer_mobileno=request.POST.get('customer_mobileno','')
    customer_total=request.POST.get('customer_total','')
    customer=Customer_Information.objects.create(customer_name=customer_name,customer_total=customer_total,customer_address=customer_address,customer_city=customer_city,customer_state=customer_state,customer_pincode=customer_pincode,customer_emailid=customer_emailid,customer_mobileno=customer_mobileno)
    table=Table_Master.objects.filter(table_capacity__gte=customer_total)
    table_no=int(0)
    for t in table:
        if(t.table_occupied==False):
            table_no=t.table_id
            customer.table_id=table_no
            customer.save()
            t.table_occupied=True
            t.save()
            break
    if(table_no!=0):
        return render(request,'BookedTable.html',{"table_alloted":table_no})
    else:
        return render(request,'Consolation.html')

def menuitems(request):
    return render(request,'MenuItems.html')

def beverages(request):
    return render(request,'Beverages.html')

def maincourse(request):
    return render(request,'MainCourse.html')

def desert(request):
    return render(request,'Desert.html')

def foodItems(request):
    return render(request,'FoodItems.html')

@login_required(login_url='/RestaurantManagementSystem/login/')
def fooditem_form(request,fooditem_id=0):
    if request.method == 'POST' :
        if fooditem_id==0:
            form = Fooditems_DetailsForm(request.POST,request.FILES)
        else:
            fitem=Fooditems_Details.objects.get(pk=fooditem_id)
            form=Fooditems_DetailsForm(request.POST,request.FILES,instance=fitem)
        if form.is_valid():
            form.save()
        return redirect('/RestaurantManagementSystem/showfooditems/')
    else:
        if fooditem_id==0:
            form=Fooditems_DetailsForm()
        else:
            fitem=Fooditems_Details.objects.get(pk=fooditem_id)
            form = Fooditems_DetailsForm(instance=fitem)
        return render(request,'AddFoodItem.html',{'form':form})
    
@login_required(login_url='/RestaurantManagementSystem/login/')
def updateFoodItem(request,fooditem_id):
    if request.method == 'POST' :
        fitem=Fooditems_Details.objects.get(pk=fooditem_id)
        form=Fooditems_DetailsForm(request.POST,request.FILES,instance=fitem)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/RestaurantManagementSystem/showfooditems/')
    else:
        fitem=Fooditems_Details.objects.get(pk=fooditem_id)
        form = Fooditems_DetailsForm(instance=fitem)
    return render(request,'UpdateFoodItem.html',{'form':form , 'fid':fooditem_id})

@login_required(login_url='/RestaurantManagementSystem/login/')
def showFoodItems(request):
    fitems=Fooditems_Details.objects.all()
    return render(request,'FoodList.html',{'fitems':fitems})

@login_required(login_url='/RestaurantManagementSystem/login/')
def deletefooditem(request,fooditem_id):
    fitem=Fooditems_Details.objects.get(pk=fooditem_id)
    fitem.delete()
    return redirect('/RestaurantManagementSystem/showfooditems/')

def addToCart(request,fooditem_id):
    flag=False
    orders=Order_Details.objects.all()
    fitem=Fooditems_Details.objects.get(pk=fooditem_id)
    for ord in orders:
        if (ord.fooditem_id==fitem):
            ord.quantity+=1
            ord.amount=ord.quantity*ord.fooditem_price
            ord.save()
            flag=True
            return render(request,'AddToCart.html',{'fitem':fitem , 'orders':orders})
    if(flag==False):
        order=Order_Details.objects.create(order_date=datetime.now(),fooditem_id=fitem,quantity=1,fooditem_price=fitem.fooditem_price,amount=fitem.fooditem_price)
        ords=Order_Details.objects.all()
        return render(request,'AddToCart.html',{'fitem':fitem , 'orders':ords})

def addQuantity(request,order_id):
    order=Order_Details.objects.get(pk=order_id)
    order.quantity+=1
    order.amount=order.quantity*order.fooditem_price
    order.save()
    orders=Order_Details.objects.all()
    return render(request,'AddToCart.html',{'orders':orders})

def subQuantity(request,order_id):
    order=Order_Details.objects.get(pk=order_id)
    if(order.quantity==1):
        order.delete()
    else:
        order.quantity-=1
        order.amount=order.quantity*order.fooditem_price
        order.save()
    orders=Order_Details.objects.all()
    return render(request,'AddToCart.html',{'orders':orders})

def deleteFromCart(request,order_id):
    order=Order_Details.objects.get(pk=order_id)
    order.delete()
    orders=Order_Details.objects.all()
    return render(request,'AddToCart.html',{'orders':orders})

def viewCart(request):
    orders=Order_Details.objects.all()
    return render(request,'AddToCart.html',{'orders':orders})

def checkout(request):
    orders=Order_Details.objects.all()
    total=float(0)
    for order in orders:
        total+=order.amount
    return render(request,'CheckOut.html',{ 'orders':orders , 'total':total})

def backToMenu(request):
    orders=Order_Details.objects.all()
    for order in orders:
        order.delete()
    return render(request,'MenuItems.html')
    
def totalAmount(request):
    orders=Order_Details.objects.all()
    total=float(0)
    for order in orders:
        total+=order.amount
    return render(request,'AddToCart.html',{ 'orders':orders , 'total':total })

def customer_display(request):
    fitems=Fooditems_Details.objects.all()
    orders=Order_Details.objects.all()
    return render(request,'DisplayFood.html',{'fitems':fitems , 'orders':orders})

def showBeverages(request):
    bev=Category_Details.objects.filter(category_description__contains='Beverages')
    fitems=Fooditems_Details.objects.filter(category_id__in=bev)
    orders=Order_Details.objects.all()
    return render(request,'DisplayFood.html',{'fitems':fitems , 'orders':orders})

def showMainCourse(request):
    main=Category_Details.objects.filter(category_description__contains='Main Course')
    fitems=Fooditems_Details.objects.filter(category_id__in=main)
    orders=Order_Details.objects.all()
    return render(request,'DisplayFood.html',{'fitems':fitems , 'orders':orders})

def showDesert(request):
    des=Category_Details.objects.filter(category_description__contains='Desert')
    fitems=Fooditems_Details.objects.filter(category_id__in=des)
    orders=Order_Details.objects.all()
    return render(request,'DisplayFood.html',{'fitems':fitems , 'orders':orders})

@login_required(login_url='/RestaurantManagementSystem/login/')
def show_customer(request):
    customers=Customer_Information.objects.all()
    return render(request,'CustomerList.html',{'customers': customers})

@login_required(login_url='/RestaurantManagementSystem/login/')
def home(request):
    return render(request,'AdminTemplate.html')

@login_required(login_url='/RestaurantManagementSystem/login/')
def employee_form(request,emp_id=0):
    if request.method == 'POST' :
        if emp_id==0:
            form = Employee_DetailsForm(request.POST,request.FILES)
        else:
            emp=Employee_Details.objects.get(pk=emp_id)
            form=Employee_DetailsForm(request.POST,request.FILES,instance=emp)
        if form.is_valid():
            form.save()
        return redirect('/RestaurantManagementSystem/showemployees/')
    else:
        if emp_id==0:
            form=Employee_DetailsForm()
        else:
            emp=Employee_Details.objects.get(pk=emp_id)
            form = Employee_DetailsForm(instance=emp)
        return render(request,'AddEmployee.html',{'form':form})

@login_required(login_url='/RestaurantManagementSystem/login/')
def showEmployees(request):
    emps=Employee_Details.objects.all()
    return render(request,'EmployeeList.html',{'emps':emps})

@login_required(login_url='/RestaurantManagementSystem/login/')
def deleteEmployee(request,emp_id):
    emp=Employee_Details.objects.get(pk=emp_id)
    emp.delete()
    return redirect('/RestaurantManagementSystem/showemployees/')

@login_required(login_url='/RestaurantManagementSystem/login/')
def updateEmployee(request,emp_id):
    emp=Employee_Details.objects.get(pk=emp_id)
    form=Employee_DetailsForm(instance=emp)
    if request.method=='POST' :
        form=Employee_DetailsForm(request.POST,instance=emp)
        if form.is_valid() :
            form.save()
            return redirect('/RestaurantManagementSystem/showemployees/')
    return render(request,'UpdateEmployee.html',{'form':form , 'eid':emp_id})

