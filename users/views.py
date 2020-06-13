import json

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CheckoutForm, ProfileRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Order, ItemSelection
from products.models import Item
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

# def handler404(request, *args, **argv):
#     return render(request, 'notfound-404.html', status=404)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            new_user = User.objects.get(username=username)
            p_form.instance=new_user.profile # Indicating who this phone number belong to.
            p_form.save()
            # print(form.cleaned_data)

            messages.success(request, f'Your account {username} has been created. You can login now.')
            return redirect('login')
    
    else:
        form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    return render(request, 'user-page-register.html', {'form': form, 'p_form': p_form})

def home(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    if request.method == 'POST': # Check if we trying to POST data, which means we are trying to save data.
        # So we will save what we have just entered to forms.
        # We add request.POST to pass in the post data (Truyền đi dữ liệu mới nhập)
        # It's necessary to add request.POST unless the data won't be updated in the box data BUT IT'S NOT BEEN SAVED YET.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # Now we check the forms validation and if they are, save them.
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account profile has been updated!')
            return redirect('profile')

    else: # This case we are trying to get the page only.
        # Give argument "instance" to give current user info to those forms
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    contexts = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', contexts)

def get_user_pending_order(request):
    # get order for the correct user
    orders = Order.objects.filter(user=request.user, order_status='P') | Order.objects.filter(user=request.user, order_status='S')| Order.objects.filter(user=request.user, order_status='RC')
    if orders.exists():
        # get the only order in the list of filtered orders
        return orders
    return 0
    # return orders

@login_required
def orders_detail(request):
    existing_orders = get_user_pending_order(request) 
    contexts ={
        'orders': existing_orders
    }
    print(existing_orders)
    return render(request, 'users/orders_detail.html', contexts)

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order:
        order.order_status = "RC"
        order.save()
        return redirect('orders-detail')

@login_required
def checkout(request):
    checkout_items = ItemSelection.objects.filter(user=request.user, ordered=False)
    
    if not checkout_items: #No item in cart -> Not allowed to checkout.
        messages.error(request, f'You have no item to checkout.')
        return redirect('cart')

    # Check number item available before checkout.
    failed_items = []
    for item in checkout_items:
        number_left = item.item.number_item_left - item.quantity
        if number_left < 0:
            failed_items.append(item)
    if failed_items:
        messages.error(request, f'Checkout failed. We do not have enough '+ ", ".join([i.item.title for i in failed_items]) + ' .')
        return redirect('cart')

    total_cost = sum(i.get_final_price() for i in checkout_items)
    
    if request.method == 'GET':
        checkout_form = CheckoutForm(initial={
            'receiver': request.user.last_name + " " + request.user.first_name,
            'phone': request.user.profile.phone,
            'address': request.user.profile.address
            }
        )
        contexts={
            'checkout_items': checkout_items,
            'total_cost': total_cost,
            'checkout_form': checkout_form
        }
        
        return render(request, 'users/checkout.html', contexts)
    else:
        checkout_form = CheckoutForm(request.POST)
        if checkout_form.is_valid():
            receiver = checkout_form.cleaned_data['receiver']
            phone = checkout_form.cleaned_data['phone']
            address = checkout_form.cleaned_data['address']

            new_order = Order.objects.create(
                user=request.user,
                receiver=receiver,
                phone=phone,
                address=address
            )

            for item in checkout_items:
                new_order.items_ordered.add(item)
                # Decreasing number of item left NO NEED TO CHECK NUMBER IS VALID HERE, CHECKED ABOVE.
                item.item.number_item_left -= item.quantity
                item.item.number_item_sold += item.quantity
                item.item.save()
                # Change ItemSelection 'ordered' to True 
                item.ordered=True
                item.save()

            messages.success(request, f'Checkout successfully. Your order will be delivery soon.')
            return redirect('cart')
        else:
            messages.error(request, f'Checkout failed. Check your info and try again.')
            return redirect('checkout')

@login_required
def cart(request):
    selected_items = ItemSelection.objects.filter(user=request.user,ordered=False)
    total_cost = sum(i.get_final_price() for i in selected_items)
    old_cost = sum(i.get_total_item_price() for i in selected_items)
    contexts={
            'selected_items':selected_items,
            'total_cost': total_cost,
            'old_cost': old_cost,
    }
    return render(request, 'cart.html', contexts)


'''
ItemSelection sẽ là item trong cart, có user có trạng thái ordered và trỏ tới item
Khi checkout, ItemSelection sẽ có ordered = True, lúc này tạo order mới.
'''
@login_required
def add_to_cart(request, pk):
    # Get the id of item
    item = get_object_or_404(Item, pk=pk)
    # user_profile = get_object_or_404(Profile, user=request.user)
    # Create a new ItemSelection if adding item is not exist in cart.
    selected_item, created = ItemSelection.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    # If created a new itemselection -> there is no similar item in cart
    # If not, selected item quantity +1.
    if not created: 
        selected_item.quantity += 1
        selected_item.save()
    messages.info(request, "This item was added to your cart.")
    return redirect('item-detail', pk)


@login_required
def remove_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    try: #Case: Having this item in cart
        selected_item = ItemSelection.objects.get(
                item=item,
                user=request.user,
                ordered=False
        )
        selected_item.delete()
        messages.info(request, "This item quantity was updated.")
    except: #Case: Not have this item in cart
        messages.info(request, "This item was not in your cart")
    return redirect('cart')

@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    try: #Case: Having this item in cart
        selected_item = ItemSelection.objects.get(
                item=item,
                user=request.user,
                ordered=False
        )
        if selected_item.quantity > 1:
            selected_item.quantity -= 1
            selected_item.save()
        else:
            selected_item.delete()
        messages.info(request, "This item quantity was updated.")
    except: #Case: Not have this item in cart
        messages.info(request, "This item was not in your cart")
    return redirect('item-detail', pk)

def to_dict(data, owner, count=None):
    return dict(
        data=data,
        count=count,
        owner=owner)

def response_api(request):
    temp = Item.objects.values('id','category','title', 'price', 'tag')
    # Data chỉ nhận mỗi kiểu: list bên trong nó là dict (hình như <=> json) ?
    return JsonResponse(
        data=list(temp),
        content_type='application/json', status=200, safe=False)