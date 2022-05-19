from django.urls import path
from .views import home,bycategory,new_details,reaction,comment,login_view,log_out,registration
urlpatterns=[
    path('',login_view,name='login'),
    path('new/',home,name='new'),
    path('<int:id>/', new_details,name='new_details'),
    path('category/<int:id>/', bycategory, name='bycategory'),
    path('reaction/<int:id>/<str:react>',reaction,name='setreaction'),
    path('comment/<int:id>',comment,name='comment'),
    path('logout/', log_out, name='logout'),
    path('registration/',registration,name='registration')
]