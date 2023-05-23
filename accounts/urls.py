from django.urls import path , include
from . import views
urlpatterns=[
    path('',views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('myAccount/',views.myAccount,name="myAccount"),
    path ('custDashboard/',views.custDashboard,name="custDashboard"),
    path ('vendorDashboard/',views.vendorDashboard,name="vendorDashboard"),
    
    
    path('vendor/', include('vendor.urls')),
]