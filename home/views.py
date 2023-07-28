import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from home.models import product, account
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
import json
import shutil

# Create your views here.
def index(request):
    products = product.objects.all()
    return render(request, 'index.html', {'products': products})

def shop(request):
    products = product.objects.all()
    products_ = list(product.objects.all().values())  # Convert queryset to a list of dictionaries
    products_json = json.dumps(products_)
    
    return render(request, 'shop.html', {'products_json': products_json, 'products': products})

def product_single(request, product_id):
    product_get = get_object_or_404(product, id=product_id)
    # SELECT product_get FROM product WHERE id = productid 
    return render(request, 'product-single.html', {'product': product_get})

def add_to_cart(request):
    quantity = int(request.GET.get('quantity'))
    if quantity > 0:
        product_id = request.GET.get('product_id')
        product_ = get_object_or_404(product, id=product_id)

        cart = request.session.get('cart', {})
        if product_id in cart:
            # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng sản phẩm lên 1
            cart[product_id]['quantity'] += quantity
        else:
            # Nếu sản phẩm chưa có trong giỏ hàng, thêm sản phẩm vào giỏ hàng
            cart[product_id] = {
                'name': product_.name,
                'price': int(product_.sale_price),
                'quantity': quantity,
                'image': product_.image
            }
        
        for product_id in cart:
            print("amount" + str(cart.get(product_id, {}).get('quantity')))

        request.session['cart'] = cart
    return JsonResponse({'success': True})

def remove_product(request):
    cart = request.session.get('cart')
    pid = request.GET.get('productid')
    if cart is not None:
        if pid in cart:
            del cart[pid]
    else:
        return JsonResponse({'success': False})


    total = 0
    for product_id in cart:
        total += cart.get(product_id, {}).get('quantity') * cart.get(product_id, {}).get('price')

    request.session['cart'] = cart
    return JsonResponse({'success': True})
    
def cart(request):
    total = 0
    cart = request.session.get('cart')
    if cart is not None:
        for product_id in cart:
            total += cart.get(product_id, {}).get('quantity') * cart.get(product_id, {}).get('price')

    return render(request,'cart.html', {'total': total})

def panel(request):
    products = product.objects.all()
    if 'account_id' not in request.session:
        return redirect('toHome')
    else:
        account_ = account.objects.get(id=request.session.get('account_id'))
        if account_.admin == False:
            return redirect('toHome')

    return render(request, 'panel.html', {'products': products})

def displayProduct(request):
    checked = request.GET.get('checked')
    productid = int(request.GET.get('product_id'))

    product_ = product.objects.get(id=productid)
    product_.display = 1 if checked == 'true' else 0
    product_.save()
    return JsonResponse({'success': True})

def getProduct(request):
    productid = int(request.GET.get('product_id'))

    product_ = get_object_or_404(product, id=productid)
    
    return JsonResponse({'success': True, 'product': serialize('json', [product_])})

@csrf_exempt
def updateProduct(request):
    data = json.loads(request.body)

    product_id = data.get('productId')

    product_ = product.objects.get(id=product_id)

    product_.name = data.get('productName')
    product_.price = data.get('productPrice')
    product_.sale_price = data.get('productSale')
    product_.amount = data.get('productQuantity')
    product_.desc = data.get('productDesc')
    product_.save()

    return JsonResponse({'success': True})

@csrf_exempt
def createProduct(request):
    # data = json.loads(request.body)
    image_file = request.FILES.get('imageFile')
    print(request.POST.get('productData'))
    product_data = json.loads(request.POST.get('productData'))



    if image_file:
        # Lưu file hình ảnh vào thư mục đích
        media_root = settings.MEDIA_ROOT
        image_path = os.path.join(media_root, image_file.name)

        # Di chuyển file đến thư mục đích
        with open(image_path, 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        product_ = product(name=product_data.get('productName'), price=product_data.get('productPrice'), sale_price=product_data.get('productSale'), amount=product_data.get('productQuantity'), desc=product_data.get('productDesc'), image=image_file.name)
        product_.save()
        print("Lưu file thành công")
        
        return JsonResponse({'success': True})
    else:
        print("Lưu file lỗi")
        return JsonResponse({'error': 'image-error'})


@csrf_exempt
def signup(request):
    return render(request, 'sign-up.html')

@csrf_exempt
def handleSignup(request):
    data = json.loads(request.body)
    print(data)
    print(data.get('username'))

    account_ = account.objects.filter(username=data.get('username')).exists()
    if account_ == False:
        user = account(username = data.get('username'), password = data.get('password'), email = data.get('email'))
        user.save()
        return JsonResponse({'success': True})
        print("Tài khoản chưa tồn tại có thể đăng kí")
    else:
        print("Tài khoản đã tồn tại")
        return JsonResponse({'success': False})
    

@csrf_exempt
def login(request):
    return render(request, 'login.html')

@csrf_exempt
def handleLogin(request):
    data = json.loads(request.body)

    username = data.get('username')
    account_ = account.objects.filter(username=username).first()
    if account_ is not None:
        if data.get('password') == account_.password:
            request.session['account_id'] = account_.id
            request.session['username'] = account_.username
            
            if account_.admin:
                return JsonResponse({'success': True, 'admin': '1'})
            else:
                return JsonResponse({'success': True, 'admin': '0'})
        else:
            return JsonResponse({'error': 'wrong-password'})
    else:
        print("That bai")
        return JsonResponse({'success': False})
    
def logout(request):
    if 'account_id' in request.session:
        del request.session['account_id']
        del request.session['username']
        if 'cart' in request.session:
            del request.session['cart']
        
    return redirect('toHome')

@csrf_exempt
def deleteProduct(request):
    productid = request.POST.get('product_id')
    product_ = product.objects.get(id=productid)
    if product is not None:
        product_.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'not-exist'})
    
def clearCart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('toHome')