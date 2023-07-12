from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View

from products.forms import ProductForm
from products.models import Product, Category, ProductImage, Cart, CartItem


# Create your views here.

# class ProductList(ListView):
#     queryset = Product.objects.all()
#     template_name = 'product/product_list.html'
#     context_object_name = 'products'

@login_required(login_url='user/login')
def product_list(request):
    products = Product.objects.all()
    for product in products:
        for i in product.productimage_set.all():
            result = i
    context = {
        'products': products,
        'productimage': result
    }
    return render(request, 'product/product_list.html', context)


def edit_contact(request, pk):
    prodcut = get_object_or_404(Product, id=pk)
    context = {
        'product': prodcut,
        'categories': Category.objects.all()
    }
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            prodcut.title = request.POST['title']
            prodcut.price = request.POST['price']
            prodcut.save()
            image = get_object_or_404(ProductImage, product_id=pk)
            image.image = request.FILES.get('images')
            image.save()
        else:
            print(form.errors)
        return redirect('/')
    return render(request,'product/product_detail.html', context)


# @permission_required('apps.add_product')
# def add_product(request):
#     categorys = Category.objects.all()
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.instance.author = request.user
#             product = form.save()
#             for image in request.FILES.getlist('images'):
#                 ProductImage.objects.create(image=image, product=product)
#
#         return redirect('/')
#     return render(request, 'product/add_product.html', {'categorys': categorys})

# @login_required
def add_product(request):
    category = Category.objects.all()
    data = request.POST
    if request.method == 'POST':
        form = ProductForm(data, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(image=image, product=product)
        print(form.errors)
        return redirect('/')
    context = {
        'category': category
    }
    return render(request, 'product/add_product.html', context)


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = '/'


class AddCartCreateView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        CartItem.objects.create(
            product=product,
            price=product.price,
            cart=cart
        )
        return redirect('product_list')


class ShowCart(ListView):
    queryset = CartItem.objects.all()
    template_name = 'product/karzinka.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user, is_active=True).first()
        return CartItem.objects.filter(cart=cart)


def delete_showcard(request, pk):
    caritem = CartItem.objects.filter(id=pk)
    caritem.delete()
    return redirect('cart')
