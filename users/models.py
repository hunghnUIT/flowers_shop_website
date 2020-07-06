from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator
from products.models import Item
from django.utils import timezone
from django.urls import reverse

ORDER_STATUS_CHOICES = (
    ('1', 'Waiting Confirmation'),
    ('2', 'Processing'),
    ('3', 'Shipping'),
    ('4', 'Completed'),
    ('5', 'Requesting Cancel'),
    ('6', 'Canceled'), #Accepted cancellation request
)

class Profile(models.Model):
    # One user has only one profile and the same in return.
    # If user were delete, the profile will be the same.
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    address = models.CharField(default='',max_length=200)
    phone = models.CharField(default='',max_length=12)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # This func is overriding save() func already exists in parent class to resize profile pics
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs) # Call save() of parent

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class ItemSelection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    price_client_bought = models.PositiveIntegerField(default=0)
    
    ''' EXPLAIN "client_bought_price" attribute:
    - When clients add a item to cart, use item.price*quantity for calculating the total price
    - But when clients bought item, this item's price is: client_bought_price, which is = item.price
    - And then the total is client_bought_price*quantity.
    (*)NOTE: This attribute's value client_bought_price wont be change once clients confirm their order
    '''

    def __str__(self):
        return self.item.title + " - Quantity: " + str(self.quantity)

    def get_total_item_price(self):
        return self.item.price * self.quantity

    def get_final_price(self):
        if self.item.discount_percent:
            return self.get_total_item_price() - int(self.get_total_item_price()*self.item.discount_percent)
        return self.get_total_item_price()


class Order(models.Model):
    # This is orders of a user. -> one user to many order.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30)
    # This have to have a link to products
    items_ordered = models.ManyToManyField(ItemSelection)
    date_ordered = models.DateTimeField(default = timezone.now())
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=2,null=False,default='1')
    address = models.CharField(max_length=70)
    phone = models.CharField(max_length=12)

    # Not allow to change order status backward.
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        original = Order.objects.filter(pk=self.pk)
        if original:
            if int(self.order_status) < int(original[0].order_status):
                self.order_status = original[0].order_status
        super(Order, self).save(force_insert, force_update,*args, **kwargs)

    def __str__(self):
        return self.user.last_name + " " + self.user.first_name + " ordered " + ", ".join([i.item.title for i in self.items_ordered.all()])

    def get_cart_items(self):
        return self.items_ordered.all()

    def get_total_order_price(self):
        return sum([i.price_client_bought*i.quantity for i in self.items_ordered.all()])

    get_total_order_price.short_description = 'Total cost'

    def get_user_fullname(self):
        return self.user.last_name + " " + self.user.first_name

    def get_cancel_order_url(self):
        return reverse("request-cancel-order",kwargs={
            'pk' : self.pk
        })
