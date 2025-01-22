from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Count
from django.template.loader import render_to_string
from django.contrib import messages
from taggit.models import Tag
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Coupon
from userauth.models import Contact, Profile
from .forms import ProductReviewForm

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth
import stripe


def index(request):
    # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter(product_status='published', featured=True)

    context = {
        'products': products
    }
    return render(request, 'main/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status='published')

    context = {
        'products': products
    }
    return render(request, 'main/product-list.html', context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    reviews = ProductReview.objects.filter(product=product).order_by('-date')

    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product review form
    review_form = ProductReviewForm()

    # Allow user to comment on more than 1 product
    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {
        'product': product,
        'p_image': p_image,
        'products': products,
        'reviews': reviews,
        'make_review': make_review,
        'review_form': review_form,
        'average_rating': average_rating,
    }
    return render(request, 'main/product-detail.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'main/category-list.html', context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)

    context = {
        'category': category,
        'products': products
    }
    return render(request, 'main/category-product-list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors
    }
    return render(request, 'main/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status='published')

    context = {
        'vendor': vendor,
        'products': products
    }
    return render(request, 'main/vendor-detail.html', context)


def tag_list_view(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        'products': products,
        'tag': tag,
    }
    return render(request, 'main/tag.html', context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    print(request.POST)

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_review = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_review': average_review
        }
    )


def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by('-date')

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'main/search.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET["min_price"]
    max_price = request.GET["max_price"]

    products = Product.objects.filter(product_status='published').order_by('-id').distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()


    data = render_to_string('main/async/product-list.html', {'products': products})
    
    return JsonResponse({"data": data})


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({
        "data": request.session['cart_data_obj'],
        "totalCartItems": len(request.session['cart_data_obj'])
    })


def cart_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "main/cart.html",
        {
            "cart_data": request.session['cart_data_obj'],
            "totalCartItems": len(request.session['cart_data_obj']),
            "cart_total_amount": cart_total_amount
        })
    else:
        messages.warning(request, 'Your cart is empty')
        return redirect('main:index')


def delete_from_cart(request):
    product_id = str(request.GET['id'])
        
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string('main/async/cart-list.html',
    {
        "cart_data": request.session['cart_data_obj'],
        "totalCartItems": len(request.session['cart_data_obj']),
        "cart_total_amount": cart_total_amount
    })

    return JsonResponse(
        {
            "data": context,
            "totalCartItems": len(request.session['cart_data_obj'])
        })


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
        
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[product_id]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string('main/async/cart-list.html',
    {
        "cart_data": request.session['cart_data_obj'],
        "totalCartItems": len(request.session['cart_data_obj']),
        "cart_total_amount": cart_total_amount
    })

    return JsonResponse(
        {
            "data": context,
            "totalCartItems": len(request.session['cart_data_obj']),
            "cart_total_amount": cart_total_amount
        })

"""
@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    # Checking if cart_data_object session exists
    if 'cart_data_obj' in request.session:
        # Getting total amount for PayPal amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
            
        # Creating CartOrder object
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount
        )

        # Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 

            cart_order_products = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE-NO-" + str(order.id), #INVOICE-NO-5
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price'])
            )
    
    host = request.get_host() # get domain url
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": cart_total_amount,
        "item_name": "Order-Item-No-" + str(order.id),
        "invoice": "INVOICE-NO-" + str(order.id),
        "currency_code": "USD",
        "notify_url": "http://{}{}".format(host, reverse('main:paypal-ipn')),
        "return_url": "http://{}{}".format(host, reverse('main:payment-successful')),
        "cancel_url": "http://{}{}".format(host, reverse('main:payment-failed')),
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    # cart_total_amount = 0   
    # if 'cart_data_obj' in request.session:
    #     for p_id, item in request.session['cart_data_obj'].items():
    #         cart_total_amount += int(item['qty']) * float(item['price'])
    
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "There are multiple addressses, only one should be activated.")
        active_address = None

    return render(request, "main/checkout.html",
        {
            "cart_data": request.session['cart_data_obj'],
            "totalCartItems": len(request.session['cart_data_obj']),
            "cart_total_amount": cart_total_amount,
            "paypal_payment_button": paypal_payment_button,
            "active_address": active_address
        })

"""

def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        request.session["full_name"] = full_name
        request.session["mobile"] = mobile
        request.session["email"] = email
        request.session["address"] = address
        request.session["city"] = city
        request.session["state"] = state
        request.session["country"] = country

        if 'cart_data_obj' in request.session:
            # Getting total amount for PayPal amount
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])
                
            # Creating CartOrder object
            order = CartOrder.objects.create(
                user = request.user,
                price = total_amount,
                full_name = full_name,
                email = email,
                phone = mobile,
                address = address,
                city = city,
                state = state,
                country = country,
            )

            # delete from session after it has already been saved in the db
            del request.session["full_name"]
            del request.session["mobile"]
            del request.session["email"]
            del request.session["address"]
            del request.session["city"]
            del request.session["state"]
            del request.session["country"]

            # Getting total amount for the cart
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price']) 

                cart_order_products = CartOrderItems.objects.create(
                    order = order,
                    invoice_no = "INVOICE-NO-" + str(order.id), #INVOICE-NO-5
                    item = item['title'],
                    image = item['image'],
                    qty = item['qty'],
                    price = item['price'],
                    total = float(item['qty']) * float(item['price'])
                )
        
        return redirect("main:checkout", order.oid)
    
    return redirect("main:checkout", order.oid)


def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order=order)

    if request.method == "POST":
        code = request.POST.get("code")
        coupon = Coupon.objects.filter(code=code, active=True).first()
        if coupon:
            if coupon in order.coupon.all():
                messages.warning(request, "Coupon already activated")
                return redirect("main:checkout", order.oid)
            else:
                discount = order.price * coupon.discount / 100
                order.coupon.add(coupon)
                order.price -= discount
                order.saved += discount
                order.save()

                messages.success(request, "Coupon Activated")
                return redirect("main:checkout", order.oid)
        else:
            messages.error(request, "Coupon doesnt exist")
            return redirect("main:checkout", order.oid)



    context = {
        "order": order,
        "order_items": order_items,
    }

    return render(request, "main/checkout.html", context)


@login_required
def payment_successful_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if order.payment_status == False:
        order.payment_status == True
        order.save()

    context = {
        "order": order,
    }

    return render(request, "main/payment-successful.html", context)


"""
@login_required
def payment_successful_view(request):
    cart_total_amount = 0   
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    return render(request, "main/payment-successful.html",
        {
            "cart_data": request.session['cart_data_obj'],
            "totalCartItems": len(request.session['cart_data_obj']),
            "cart_total_amount": cart_total_amount,
        })
"""

@login_required
def payment_failed_view(request):
    return render(request, 'main/payment-failed.html')


@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)

    # chart
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user = request.user,
            mobile = mobile,
            address = address
        )
        messages.success(request, "Address Added Succesfully.")
        return redirect("main:dashboard")
    else:
        print("Error")

    # profile
    profile = Profile.objects.get(user=request.user)

    context = {
        "orders": orders,
        "orders_list": orders_list,
        "profile": profile,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'main/dashboard.html', context)


def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)
    context = {
        "order_items": order_items
    }
    return render(request, 'main/order-detail.html', context)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False) # set all address status to False
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


@login_required
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.all()
    except:
        wishlist = None
    
    context = {
        "wishlist": wishlist
    }
    return render(request, "main/wishlist.html", context)


@login_required
def add_to_wishlist(request):
    product_id = request.GET["id"]
    product = Product.objects.get(id=product_id)

    context = {}
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True
        }

    return JsonResponse(context) 
    

def delete_from_wishlist(request):
    pid = request.GET["id"]
    Wishlist.objects.filter(id=pid, user=request.user).delete()

    wishlist = Wishlist.objects.filter(user=request.user)

    context = {
        "bool": True,
        "wishlist": wishlist
    }
    wishlist_json = serializers.serialize("json", wishlist)
    data = render_to_string("main/async/wishlist-list.html", context)
    return JsonResponse({
            "data": data,
            "wishlist": wishlist_json,
        })


def contact(request):
    return render(request, "main/contact.html")


def ajax_contact(request):
    full_name = request.GET["full_name"]
    email = request.GET["email"]
    phone = request.GET["phone"]
    subject = request.GET["subject"]
    message = request.GET["message"]

    contact = Contact.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message sent successfully"
    }

    return JsonResponse({"data": data})





def about_us(request):
    return render(request, "main/about_us.html")

def purchase_guide(request):
    return render(request, "main/purchase_guide.html")

def privacy_policy(request):
    return render(request, "main/privacy_policy.html")

def terms_of_service(request):
    return render(request, "main/terms_of_service.html")








