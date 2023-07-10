from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm



class SellerForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': "form-control form-control-sm"}))
    password2 = forms.CharField(label='Повторіть Пароль', widget=forms.PasswordInput(attrs={'class': "form-control form-control-sm"}))
    hometown_add = forms.BooleanField(label='Розширені можливості', required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input", 'type': "checkbox", 'role': "switch"}))

    class Meta:
        model = Seller
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2', 'hometown_add']

        labels = {
            'username': "Логін",
            'first_name': "Им'я",
            'last_name': 'Фамілія',
            'email': "Email",
            'phone': 'Номер Телефону',
        }
        help_texts = {'username': ""}


        widgets={
                "username": forms.TextInput(attrs={'class': "form-control form-control-sm ", 'autocomplete': "off"}),
                "first_name": forms.TextInput(attrs={'class': "form-control form-control-sm ", 'autocomplete': "off"}),
                "last_name": forms.TextInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),
                "phone": forms.NumberInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),
                "email": forms.TextInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),
                }


    def save(self, commit=True):
        user = super(SellerForm, self).save(commit=False)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.set_password(self.cleaned_data['password2'])
        user.is_active = self.cleaned_data.get('is_active', True)
        user.is_staff = self.cleaned_data.get('is_staff', False)
        hometown_add = self.cleaned_data.get('hometown_add', False)
        if commit:
            user.save()
        if hometown_add:
            seller_group = Group.objects.get(name='hometown')
            user.groups.set([seller_group])
        return user



class Form(forms.ModelForm):
    code_ord = forms.CharField(required=False, label='КОД Продукту',
                               widget=forms.TextInput(attrs={'class': "form-control form-control-sm"}))
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Назва Продукту', required=False,
                                     empty_label="Виберіть назву продукту", widget=forms.Select(attrs={'class': "form-select form-select-sm filter-forms"}))
    delivery = forms.ChoiceField(label='Доставка', choices=(('pickup', 'САМОВИВІЗ'), ('NP', 'НОВА ПОШТА')),
                                 widget=forms.RadioSelect(attrs={'id': "delivery"}), initial='pickup')

    class Meta:
        model = Order
        fields = ['code_ord', 'product', 'amount', 'sizes', 'delivery', 'name_client', 'phone_client', 'city_client', 'dep_np', 'actual_weight', 'status', 'sum']
        labels = {
            "code_ord": "КОД",
            'product': 'Назва',
            'amount': 'Кількість',
            'sizes': 'Розміри',
            'name_client': 'ПІБ Отримувач',
            'phone_client': 'Телефон Отримувача',
            'city_client': ' Місто Отримувача',
            'dep_np': 'Відділення Нової пошти',
            'actual_weight': 'Фактична Вага',
            'status': 'Статус',
            'sum': "Вартість",
        }
        widgets={
                "sizes": forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                'name_client': forms.TextInput(attrs={'class': "form-control form-control-sm", 'id': "name_client", 'autocomplete': "off"}),
                'phone_client': forms.TextInput(attrs={'class': "form-control form-control-sm", 'id': "phone_client", 'autocomplete': "off"}),
                'city_client': forms.TextInput(attrs={'class': "form-control form-control-sm", 'id': "city_client", 'autocomplete': "off"}),
                'dep_np': forms.TextInput(attrs={'class': "form-control form-control-sm", 'id': "dep_np", 'autocomplete': "off"}),
                'actual_weight': forms.Select(attrs={'class ': "form-select form-select-sm filter-forms", 'id': "id_weight"}),
                'status': forms.Select(attrs={'class': "form-select form-select-sm filter-forms", 'id': "id_status"}),
                'amount': forms.NumberInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),
                'sum': forms.NumberInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),

                }



    def clean(self):
        cleaned_data = super().clean()
        code_ord = cleaned_data.get("code_ord")
        amount = cleaned_data.get("amount")
        product = cleaned_data.get("product")
        delivery = cleaned_data.get("delivery")
        name_client = cleaned_data.get("name_client")
        phone_client = cleaned_data.get("phone_client")
        city_client = cleaned_data.get("city_client")
        dep_np = cleaned_data.get("dep_np")
        sum = cleaned_data.get("sum")
        if not code_ord and not product:
            raise forms.ValidationError("Вкажіть назву або код продукту")
        elif code_ord and not product:
            try:
                product = Product.objects.get(code=code_ord)
            except Product.DoesNotExist:
                raise forms.ValidationError("Продукт з таким кодом не існує")
            cleaned_data["product"] = product
        elif product and not code_ord:
            cleaned_data["code_ord"] = product.code
        if amount > product.amount:
            raise forms.ValidationError(f"Залишок товару {product.amount}")
            del amount
        elif sum < (product.cost * amount):
            raise forms.ValidationError("Помилка Вартості")
            del sum
        if delivery == "NP":
            if not name_client or not phone_client or not city_client or not dep_np:
                raise forms.ValidationError("Заповніть інформацію для Нової пошти")
        return cleaned_data


    def save(self, commit=True, request=None):
        order = super().save(commit=False)
        if self.cleaned_data['delivery'] == 'NP':
            customer, create = Customer.objects.get_or_create(
                phone=self.cleaned_data['phone_client'],
                name=self.cleaned_data['name_client'],
                address=self.cleaned_data['city_client'],
            )
            order.customer = customer
        else:
            order.customer = order.seller
            order.actual_weight = "САМОВИВІЗ"
            order.status = 'САМОВИВІЗ'
            order.status_code = '0'

        if commit:
            order.save()
        return order

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.exclude(amount=0)



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            "code": "КОД",
            'name': 'Назва',
            'amount': 'Кількість',
            'cost': 'Ціна за 1 од.',
            'img': "Зображення продукту"
        }
        widgets={
                "code": forms.TextInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),
                "name": forms.TextInput(attrs={'class': "form-control form-control-sm form-control-wrap text-truncate", 'autocomplete': "off"}),
                "amount": forms.NumberInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),
                "cost": forms.NumberInput(attrs={'class': "form-control form-control-sm", 'autocomplete': "off"}),
                "img": forms.FileInput(attrs={'class': 'form-control form-control-sm'})
        }




        
