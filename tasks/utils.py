from .models import Product, Order, OrderItem, Post, Comment
from django.db.models import Sum, F
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist


# *********** inventory management system ****************
def add_product(name, quantity, price):
    """
    Adds a new product to the inventory.
    
    :param name: Name of the product
    :param quantity: Quantity of the product
    :param price: Price of the product
    :return: The created Product object
    """
    product = Product(name=name, quantity=quantity, price=price)
    product.save()
    return product

def update_product_quantity(product_id, quantity):
    """
    Updates the quantity of an existing product.
    
    :param product_id: ID of the product to update
    :param quantity: New quantity of the product
    :return: The updated Product object or None if the product does not exist
    """
    try:
        product = Product.objects.get(id=product_id)
        product.quantity = quantity
        product.save()
        return product
    except Product.DoesNotExist:
        return None

def calculate_total_inventory_value():
    """
    Calculates the total value of the inventory.
    
    :return: The total value of the inventory
    """
    total_value = Product.objects.aggregate(total_value=Sum(F('quantity') * F('price')))['total_value']
    return total_value or 0

# ************** end of inventory management system **************




# **************  function for odering system  *****************

def create_order(user):
    order = Order.objects.create(user=user)
    return order

def add_item_to_order(order, product_id, quantity):
    product = Product.objects.get(id=product_id)
    item = OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price * quantity)
    order.total_price += item.price
    order.save()
    return item
#    ot = {"product_id": 1,"quantity": 2}


def calculate_order_total(order_id):
    order = Order.objects.get(id=order_id)
    return order.total_price


# ***** blog platform *****


def create_post(title, content, author):
    post = Post.objects.create(title=title, content=content, author=author)
    return post

def add_comment_to_post(post, author, content):
    comment = Comment.objects.create(post=post, author=author, content=content)
    return comment

def fetch_comments_for_post(post_id):
    print("outside of this try block")
    try:
        post = Post.objects.get(id=post_id)
        comments = post.comments.all()
        return comments
    except ObjectDoesNotExist as e:
        print(f"Error: {e}")
        return []
