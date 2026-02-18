from django.urls import path
from .views import add_to_cart, view_cart, update_cart, remove_from_cart

urlpatterns = [
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', update_cart, name='update_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    

]


from .views import checkout, my_orders

urlpatterns += [
    path('checkout/', checkout, name='checkout'),
    path('my-orders/', my_orders, name='my_orders'),
]
