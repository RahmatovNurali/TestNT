from django.urls import path

from products.views import add_product, ProductDeleteView, edit_contact, ShowCart, AddCartCreateView, \
    delete_showcard, product_list

urlpatterns = [
    path('', product_list, name='product_list'),
    path('add_product', add_product, name='add_product'),
    path('product-delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('product-detail/<int:pk>', edit_contact, name='product_detail'),
    path('cart', ShowCart.as_view(), name='cart'),
    path('add-cart/<int:pk>', AddCartCreateView.as_view(), name='add_cart'),
    path('delete_showcard/<int:pk>', delete_showcard, name='showcart_delete'),
]
