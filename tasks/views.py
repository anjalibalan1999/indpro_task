from .models import User, Order, Post, Comment, Product
from .utils import create_post, add_comment_to_post, fetch_comments_for_post
from .utils import add_product, update_product_quantity, calculate_total_inventory_value
from .utils import create_order, add_item_to_order, calculate_order_total

from django.http import Http404, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json



# inventory project *********************
@csrf_exempt
def add_product_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            quantity = data.get('quantity')
            price = data.get('price')
            product = add_product(name, quantity, price)
            return JsonResponse({'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def update_product_quantity_view(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity')
            product = update_product_quantity(product_id, quantity)
            if product:
                return JsonResponse({'id': product.id, 'name': product.name, 'quantity': product.quantity, 'price': product.price})
            else:
                return JsonResponse({'error': 'Product not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])

def get_inventory_value_view(request):
    if request.method == 'GET':
        total_value = calculate_total_inventory_value()
        return JsonResponse({'total_inventory_value': total_value})
    else:
        return HttpResponseNotAllowed(['GET'])

# ********************   end of inevntory management system **********************



# ******* user management system *********

@csrf_exempt
def create_user_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            if not username or not email:
                return JsonResponse({'error': 'Username and email are required'}, status=400)
            user = User.objects.create(username=username, email=email)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def update_user_view(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            try:
                user = User.objects.get(id=user_id)
                if username:
                    user.username = username
                if email:
                    user.email = email
                user.save()
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at.isoformat()
                })
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])

def get_user_view(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['GET'])
    
# ********** End of User management system ***********


# ******** order processing system *********

@csrf_exempt
def create_order_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = get_object_or_404(User, id=user_id)
            order = create_order(user)
            return JsonResponse({'order_id': order.id, 'total_price': float(order.total_price)})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def add_item_to_order_view(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity')
            order = get_object_or_404(Order, id=order_id)
            item = add_item_to_order(order, product_id, quantity)
            return JsonResponse({'order_id': order.id, 'item_id': item.id, 'total_price': float(order.total_price)})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['POST'])

def get_order_total_view(request, order_id):
    if request.method == 'GET':
        try:
            total_price = calculate_order_total(order_id)
            return JsonResponse({'order_id': order_id, 'total_price': float(total_price)})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['GET'])
    
# ******* end of order processing system  ********


# ****** blog plateform  ********

@csrf_exempt
def create_post_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')
            author_id = data.get('author_id')
            author = get_object_or_404(User, id=author_id)
            post = create_post(title, content, author)
            return JsonResponse({'post_id': post.id, 'title': post.title, 'content': post.content, 'author_id': post.author.id, 'created_at': post.created_at})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def add_comment_view(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            author_id = data.get('author_id')
            author = get_object_or_404(User, id=author_id)
            post = get_object_or_404(Post, id=post_id)
            comment = add_comment_to_post(post, author, content)
            return JsonResponse({'comment_id': comment.id, 'post_id': post.id, 'author_id': comment.author.id, 'content': comment.content, 'created_at': comment.created_at})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except (User.DoesNotExist, Post.DoesNotExist):
            return JsonResponse({'error': 'Author or Post not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def get_comments_view(request, post_id):
    if request.method == 'GET':
        print("outside")
        try:
            comments = fetch_comments_for_post(post_id)
            print(comments)
            comments_data = [{'id': comment.id, 'author_id': comment.author.id, 'content': comment.content, 'created_at': comment.created_at} for comment in comments]
            return JsonResponse({'post_id': post_id, 'comments': comments_data})
        except Http404:
            return JsonResponse({'error': 'Post not found or no comments available'}, status=404)
    else:
        return HttpResponseNotAllowed(['GET'])