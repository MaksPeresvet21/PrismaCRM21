from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission



class Seller(AbstractUser):

    phone = models.CharField(max_length=10, verbose_name="Номер телефону", blank=False, null=False)


    def __str__(self):
        return self.username

class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=100, null=True, verbose_name="КОД", unique=True)
    name = models.CharField(max_length=100, null=True, verbose_name="Назва")
    img = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Зображення', default='images/t6yYGXFWbDE.jpg')
    amount = models.IntegerField(null=True)
    cost = models.FloatField(null=True)
    total = models.FloatField(null=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")

    def save(self, *args, **kwargs):
        self.total = self.amount * self.cost
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name



class Order(models.Model):
    code_ord = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, related_name='orders_by_product', null=True, on_delete=models.CASCADE,)
    amount = models.IntegerField(null=True)
    sizes = models.CharField(max_length=50, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    name_client = models.CharField(max_length=50, blank=True, null=True)
    phone_client = models.CharField(max_length=13, blank=True, null=True)
    city_client = models.CharField(max_length=200, blank=True, null=True)
    dep_np = models.CharField(max_length=200, blank=True, null=True)
    actual_weight = models.CharField(max_length=10, blank=False, choices=(('1', '1кг.'), ('2', '2кг.'), ('4', '4кг.')), default='1')
    number_ttn = models.CharField(max_length=200, blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)
    margin = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(('Предоплата', 'Предоплата'), ('Повна Оплата', 'Повна Оплата')), default='Предоплата')
    status_code = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def save(self, *args, **kwargs):
        if not self.id:
            if self.code_ord:
                product = Product.objects.filter(code=self.code_ord).first()
                if product:
                    self.product = product
            product_n = Product.objects.get(id=self.product.id)
            self.margin = self.sum - (self.amount * product_n.cost)
            product_n.amount -= self.amount
            product_n.save()
            if self.status != 'САМОВИВІЗ':
                customer = Customer.objects.get(id=self.customer.id)
                customer.seller = self.seller
                customer.save()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        product_n = Product.objects.get(id=self.product.id)
        product_n.amount += self.amount
        product_n.save()
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.product or self.code_ord or str(self.pk)



