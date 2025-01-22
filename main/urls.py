from django.urls import path, include

from .views import index, category_list_view, product_list_view, category_product_list_view, vendor_list_view, vendor_detail_view, product_detail_view, tag_list_view, ajax_add_review, search_view, filter_product, add_to_cart, cart_view, delete_from_cart, update_cart, payment_successful_view, payment_failed_view, customer_dashboard, order_detail, make_address_default, wishlist_view, add_to_wishlist, delete_from_wishlist, contact, ajax_contact, about_us, privacy_policy, purchase_guide, terms_of_service, checkout, save_checkout_info

app_name = 'main'

urlpatterns = [
    # Home Page
    path('', index, name='index'),

    # Products
    path('products/', product_list_view, name='product-list'),
    path('product/<pid>', product_detail_view, name='product-detail'),
    
    # Category
    path('category/', category_list_view, name='category-list'),
    path('category/<cid>/', category_product_list_view, name='category-product-list'),

    # Vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),

    # Tags
    path('products/tag/<slug:tag_slug>', tag_list_view, name='tags'),

    # Add Review
    path('ajax-add-review/<int:pid>/', ajax_add_review, name='ajax-add-review'),

    # Search 
    path('search/', search_view, name='search'),

    # Filter
    path('filter-products/', filter_product, name='filter-product'),

    # Add to cart
    path('add-to-cart/', add_to_cart, name='add-to-cart'),

    # Cart page list
    path('cart/', cart_view, name='cart'),
    
    # Delete from Cart
    path('delete-from-cart/', delete_from_cart, name='delete-from-cart'),

    # Update Cart
    path('update-cart/', update_cart, name='update-cart'),

    # Checkout
    # path('checkout/', checkout_view, name='checkout'),
    path('checkout/<oid>/', checkout, name='checkout'),

    # Paypal URL
    path('paypal/', include('paypal.standard.ipn.urls')),

    # Payment Successful
    # path('payment-successful/', payment_successful_view, name='payment-successful'), 
    path('payment-successful/<oid>/', payment_successful_view, name='payment-successful'), 

    # Payment Failed
    path('payment-failed/', payment_failed_view, name='payment-failed'), 

    # Customer Dashboard
    path('dashboard/', customer_dashboard, name='dashboard'), 

    # Order Detail
    path('dashboard/order/<int:id>', order_detail, name='order-detail'), 

    # Make Address Default
    path('make-default-address/', make_address_default, name='make-default-address'), 

    # Wishlist
    path('wishlist/', wishlist_view, name='wishlist'), 

    # Add to wishlist
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'), 

    # Delete from wishlist
    path('delete-from-wishlist/', delete_from_wishlist, name='delete-from-wishlist'), 

    # Contact
    path('contact/', contact, name='contact'), 

    # Ajax Contact Form
    path('ajax-contact-form/', ajax_contact, name='ajax-contact-form'), 

    # New Checkout Route
    path('save-checkout-info/', save_checkout_info, name='save-checkout-info'), 



]
