"""
URL configuration for VenusFancy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myfancy import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.SignUpView.as_view(),name="sign-up"),
    path("",views.SignInView.as_view(),name="sign-in"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("profile/<int:pk>/change/",views.UserProfileUpdateView.as_view(),name="profile-edit"),
    path("product/add/",views.ProductCreateView.as_view(),name="product-add"),
    # path("product/variant/add/",views.ProductVarientCreateView.as_view(),name="product-variant-add"),
    path("product/<int:pk>/detail/",views.ProductDetailView.as_view(),name="product-detail"),
    path("myproduct/all/",views.MyProductListView.as_view(),name="myproduct"),
    path("myproduct/<int:pk>/remove/",views.MyProductDeleteView.as_view(),name="myproduct-delete"),
    path("product/cart/<int:product_id>/add/",views.AddToCartView.as_view(), name="addtocart"),
    path("product/cartitems/",views.MyCartItemView.as_view(), name="mycartitems"),
    path("product/cartitems/<int:pk>/remove/",views.MyCartItemsDeleteView.as_view(), name="mycartitems-remove"),
    path("customer/details/",views.AddressView.as_view(), name="address"),
    path("product/cash/on/delivery/",views.CashOnDeliveryListView.as_view(),name="cash-on-delivery"),
    path("product/online/payment/",views.CheckOutView.as_view(),name="online-payment"),
    path("payment/verification/",views.PaymentVerificationView.as_view(),name="payment-verification"),
    path("myorder/summary/",views.MyPurchaseView.as_view(),name="myorders"),
    path("product/<int:pk>/review/add/",views.ReviewCreateView.as_view(),name="review-add"),
    path("address/<int:pk>/change/",views.AddressEditView.as_view(),name="address-edit"),
    path("product/review/<int:pk>/all/",views.ReviewListView.as_view(),name="review-all"),
    path("cash/on/delivery/<int:pk>/remove/",views.CashOndeliveryCancelView.as_view(),name="cash-on-delivery-cancel"),
    path("logout/",views.LogoutView.as_view(),name="sign-out"),
    path("materials/add/",views.MaterialCreateView.as_view(),name="material-add"),
    path("materials/<int:pk>/change/",views.MaterialUpdateView.as_view(),name="material-edit"),
    path("materials/all/",views.MaterialListView.as_view(),name="material-all"),
    path("materials/<int:pk>/remove/",views.MaterialDeleteView.as_view(),name="material-delete"),
    path("occasion/add/",views.OccasionCreateView.as_view(),name="occasion-add"),
    path("occasion/<int:pk>/change/",views.OccasionUpdateView.as_view(),name="occasion-edit"),
    path("occasion/all/",views.OccasionListView.as_view(),name="occasion-all"),
    path("occasion/<int:pk>/remove/",views.OccasionDeleteView.as_view(),name="occasion-delete"),
    path("colour/add/",views.ColourCreateView.as_view(),name="colour-add"),
    path("colour/<int:pk>/change/",views.ColourUpdateView.as_view(),name="colour-edit"),
    path("colour/all/",views.ColourListView.as_view(),name="colour-all"),
    path("colour/<int:pk>/remove/",views.ColourDeleteView.as_view(),name="colour-delete"),
    path("feature/add/",views.FeatureCreateView.as_view(),name="feature-add"),
    path("feature/<int:pk>/change/",views.FeatureUpdateView.as_view(),name="feature-edit"),
    path("feature/all/",views.FeatureListView.as_view(),name="feature-all"),
    path("feature/<int:pk>/remove/",views.FeatureDeleteView.as_view(),name="feature-delete"),
    path("type/add/",views.TypeCreateView.as_view(),name="type-add"),
    path("type/<int:pk>/change/",views.TypeUpdateView.as_view(),name="type-edit"),
    path("type/all/",views.TypeListView.as_view(),name="type-all"),
    path("type/<int:pk>/remove/",views.TypeDeleteView.as_view(),name="type-delete"),
    path("tag/add/",views.TagCreateView.as_view(),name="tag-add"),
    path("tag/<int:pk>/change/",views.TagUpdateView.as_view(),name="tag-edit"),
    path("tag/all/",views.TagListView.as_view(),name="tag-all"),
    path("tag/<int:pk>/remove/",views.TagDeleteView.as_view(),name="tag-delete"),
    path("size/add/",views.SizeCreateView.as_view(),name="size-add"),
    path("size/<int:pk>/change/",views.SizeUpdateView.as_view(),name="size-edit"),
    path("size/all/",views.SizeListView.as_view(),name="size-all"),
    path("size/<int:pk>/remove/",views.SizeDeleteView.as_view(),name="size-delete"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

