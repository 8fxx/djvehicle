"""sts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path
from vsms import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', login_required(views.vehiclelist.as_view()), name='Index'),
    
    #home
    path('', views.indexview, name='Index'),
    path('landing/', views.landingpage, name='Landing'),
    
    path('brand/<int:pk>',views.brandview, name='brand'),
    path('unit/<str:unit>',views.unitview, name='unit'),
    path('type/<str:type>',views.typeview, name='type'),
    path('<int:pk>',login_required(views.vehicledetail.as_view()),name='detail'),
    path('search/',views.search,name='search'),
    
    #vehicle
    path('addvehicle/', views.createvehicles, name='createvehicle'),
    path('addvehicle/', login_required(views.createvehicle.as_view()), name='createvehicle'),
    path('updatevehicle/<int:pk>', login_required(views.updatevehicle.as_view()), name='updatevehicle'),
    path('deletevehicle/<int:pk>', login_required(views.deletevehicle.as_view()), name='deletevehicle'),

    #status
    path('addstatus/<int:pk>', views.createstatus, name='createstatus'),
    # path('addstatus/<int:pk>', (views.AddStatus.as_view()), name='createstatus'),
    path('updatestatus/<int:pk>', views.Editstatus.as_view(), name='updatestatus'),
    path('deletestatus/<int:pk>', views.deletestatus.as_view(), name='deletestatus'),
    path('statusapprove/<int:pk>',views.statusapproval, name='approvestatus'),

    #auth
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout,name='logout'),

    #chart
    path('chart/', views.charts,name='chart')

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
