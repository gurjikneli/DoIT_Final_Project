from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Category


def dish_list(request):
    dishes = Dish.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    spicy = request.GET.get('spicy')
    no_nuts = request.GET.get('no_nuts')
    vegetarian = request.GET.get('vegetarian')

    if category_id:
        dishes = dishes.filter(category_id=category_id)

    # Spiciness filtering
    if spicy:
        dishes = dishes.filter(spicy_level=spicy)

    # No Nuts filtering
    if no_nuts == "on":
        dishes = dishes.filter(has_nuts=False)

    # Vegetarian filtering
    if vegetarian == "on":
        dishes = dishes.filter(is_vegetarian=True)

    context = {
        'dishes': dishes,
        'categories': categories
    }

    return render(request, 'menu/dish_list.html', context)


def add_to_cart(request, dish_id):
    cart = request.session.get('cart', {})
    cart[dish_id] = cart.get(dish_id, 0) + 1
    request.session['cart'] = cart
    return redirect('dish_list')


def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for dish_id, quantity in cart.items():
        dish = get_object_or_404(Dish, id=dish_id)
        subtotal = dish.price * quantity
        total += subtotal

        items.append({
            'dish': dish,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'items': items,
        'total': total
    }

    return render(request, 'menu/cart.html', context)


def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})
    if str(dish_id) in cart:
        del cart[str(dish_id)]
    request.session['cart'] = cart
    return redirect('cart')


def update_quantity(request, dish_id, action):
    cart = request.session.get('cart', {})
    dish_id = str(dish_id)

    if dish_id in cart:
        if action == "increase":
            cart[dish_id] += 1
        elif action == "decrease":
            cart[dish_id] -= 1
            if cart[dish_id] <= 0:
                del cart[dish_id]

    request.session['cart'] = cart
    return redirect('cart')
