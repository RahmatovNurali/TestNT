from django.db import models
from django.db.models import ForeignKey, CASCADE
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.utils.text import slugify

from accounts.models import User


# Create your models here.


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.ForeignKey('products.Category', models.CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey('products.Product', models.CASCADE)
    image = models.ImageField(upload_to='product/images/')


class Cart(BaseModel):
    user = models.ForeignKey('accounts.User', models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'is_active')

    @property
    def total_summa(self):
        items = self.cartitem_set.values_list('price', 'quantity')
        return sum(map(lambda i: i[0] * i[1], items))


class CartItem(BaseModel):
    product = models.ForeignKey('products.Product', models.CASCADE)
    cart = models.ForeignKey('products.Cart', models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
