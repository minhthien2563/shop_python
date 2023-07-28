from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', views.index, name='toHome'),
path('shop', views.shop, name='toShop'),
path('product/<int:product_id>', views.product_single, name='toProduct'),
path('add-to-cart', views.add_to_cart, name='add-to-cart'),
path('cart', views.cart, name='toCart'),
path('remove_product', views.remove_product, name='removeProduct'),
path('panel', views.panel, name='toPanel'),
path('displayProduct', views.displayProduct, name='displayProduct'),
path('getProductEdit', views.getProduct, name='getProductEdit'),
path('updateProduct', views.updateProduct, name='updateProduct'),
path('signup', views.signup, name='signup'),
path('handleSignup', views.handleSignup, name='handleSignup'),
path('login', views.login, name='login'),
path('handleLogin', views.handleLogin, name='handleLogin'),
path('logout', views.logout, name='logout'),
path('createProduct', views.createProduct, name='createProduct'),
path('deleteProduct', views.deleteProduct, name='deleteProduct'),
path('clearCart', views.clearCart, name='clearCart')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
