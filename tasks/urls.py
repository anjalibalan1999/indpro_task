from django.urls import path
from .views import add_product_view, update_product_quantity_view, get_inventory_value_view
from .views import create_user_view, update_user_view, get_user_view
from .views import create_order_view, add_item_to_order_view, get_order_total_view 
from .views import create_post_view, add_comment_view, get_comments_view


urlpatterns = [
    # *********** inventory management system *********
    path('products', add_product_view, name='add_product'),
    path('products/<int:product_id>', update_product_quantity_view, name='update_product_quantity'),
    path('inventory/value', get_inventory_value_view, name='get_inventory_value'),


    # ***** user management system ******
    path('users', create_user_view, name='create_user'),
    path('users/<int:user_id>', update_user_view, name='update_user'),
    path('user/<int:user_id>', get_user_view, name='get_user'),


    # ****** order processing  ******
    path('orders', create_order_view, name='create_order'),
    path('orders/<int:order_id>/items', add_item_to_order_view, name='add_item_to_order'),
    path('orders/<int:order_id>/total', get_order_total_view, name='get_order_total'),


    # ******* blog platform ********
    path('posts', create_post_view, name='create_post'),
    path('posts/<int:post_id>/comments', add_comment_view, name='add_comment'),
    path('posts/<int:post_id>/comments_list', get_comments_view, name='get_comments'),
    
]

