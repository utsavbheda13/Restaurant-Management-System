from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView
from RestaurantManagementSystem.views import bookTable,login,auth_view,loggedin,invalidlogin,logout,processTableRequest,menuitems,foodItems,fooditem_form,showFoodItems,deletefooditem,addToCart,customer_display,show_customer,home,employee_form ,showEmployees,deleteEmployee
from RestaurantManagementSystem.views import updateEmployee,updateFoodItem,index,viewCart,addQuantity,subQuantity,deleteFromCart,totalAmount,checkout,backToMenu
from RestaurantManagementSystem.views import showBeverages,showDesert,showMainCourse

urlpatterns=[
	path('',index,name='index'),
    url(r'^booktable/', bookTable,name='book_table'),
    url(r'^login/$', login, name='login'),
	url(r'^auth/$', auth_view,name='auth'),
	path('password_reset/',PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
	path('password_reset/complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
	path('password_reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
	path('password_reset/done/',PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
	url(r'^logout/$', logout,name='logout'),
	url(r'^loggedin/$', loggedin),
	url(r'^invalidlogin/$', invalidlogin),
	# url(r'^booktable/',bookTable,name='book_table'),
    url(r'^processtablerequest/', processTableRequest),
	url(r'^menuitems/',menuitems,name='menu'),
	url(r'^fooditems/',foodItems),
	url(r'^addfooditem/', fooditem_form , name='add_fooditem'),
	url(r'^showfooditems/',showFoodItems,name='list_fooditem'),
	path('<int:fooditem_id>/',updateFoodItem,name='update_fooditem'),
	path('deletefooditem/<int:fooditem_id>/',deletefooditem,name='delete_fooditem'),
	url(r'^addemployee/', employee_form , name='add_employee'),
	url(r'^showemployees/',showEmployees,name='list_employee'),
	path('updateemployee/<int:emp_id>/',updateEmployee,name='update_employee'),
	path('deleteemployee/<int:emp_id>/',deleteEmployee,name='delete_employee'),
	# url(r'^addedfooditem/',addedFoodItem)
	url(r'^viewcart/',viewCart,name='view_cart'),
	path('addtocart/<int:fooditem_id>/',addToCart,name='add_cart'),
	url(r'^customer_display/',customer_display,name='customer_display'),
	# path('continueShopping/<int:order_id>',continueShopping,name='continue_shopping')
	url(r'^showcustomerdetails/',show_customer,name='show_customer'),
	url(r'^home/',home,name='home'),
	path('addq/<int:order_id>',addQuantity,name='add_quantity'),
	path('subq/<int:order_id>',subQuantity,name='sub_quantity'),
	path('delc/<int:order_id>',deleteFromCart,name='delete_from_cart'),
	url(r'^totalamount/',totalAmount,name='total_amount'),
	url(r'^bill/',checkout,name='bill'),
	url(r'^backtomenu/',backToMenu,name='back_to_menu'),
	url(r'^showBeverages/',showBeverages,name='show_beverages'),
	url(r'^showMainCourse/',showMainCourse,name='show_maincourse'),
	url(r'^showdesert/',showDesert,name='show_desert'),
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)