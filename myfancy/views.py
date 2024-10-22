from django.shortcuts import render,redirect

from django.views.generic import View,UpdateView,CreateView,DetailView,FormView,ListView

from myfancy.forms import SignUpForm,SignInForm,UserProfileForm,ProductForm,ProductVariantForm,AddressForm,ReviewForm,MaterialForm,OccasionForm,ColourForm,FeatureForm,TypeForm,TagForm,SizeForm,AddressAddForm

from django.contrib.auth import authenticate,login,logout

from myfancy.models import Product,UserProfile,ProductVariant,Cart_items,Orders,Address,Reviews,Material,Occasion,Colour,Feature,Type,Tag,Size,Cart,AddressStore

from django.urls import reverse_lazy

from django.forms import inlineformset_factory

from django.db.models import Q

from django.utils.decorators import method_decorator

from myfancy.decorators import signin_required,admin_permission_required

from django.contrib import messages

from decouple import config

from django import forms

from django.utils import timezone

from django.core.mail import send_mail

import threading

from twilio.rest import Client


# text message sending

account_sid = config("account_sid")

auth_token = config("auth_token")

def sent_text_message(customer_name,product_name_str,total,client_number):
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_=config("from_"),
    body=    f"Hi {customer_name},\n\n Your order for {product_name_str} has been successfully placed.The total amount is ₹{total}.\n\n Thank you for shopping with us!\n\n Best regards,\n Venus Fancy",
    to=f'+91{client_number}'
    )
    print(message.sid) 
    
    
# email sending

def sent_email_message(customer_name,product_name_str,total,recipient_email):
    
    message=(
    f"Hi {customer_name},\n\n Your order for {product_name_str} has been successfully placed.The total amount is ₹{total}.\n\n Thank you for shopping with us!\n\n Best regards,\n Venus Fancy"
)
    
    subject="Order Confirmation - Your Order Has Been Successfully Placed"
    
    send_mail(
                subject,message,"ssuhaibakther12@gmail.com",[recipient_email,],fail_silently=False
            )


# inline form

ProductVariantFormSet = inlineformset_factory(
    Product,                    # Parent model
    ProductVariant,             # Model to inline
    form=ProductVariantForm,    # Form class for the inline model
    extra=6,                    # Number of empty forms to display
    can_delete=True             # Allows the deletion of existing inline instances
)

key_ID=config("key_ID")

key_SECRET=config("key_SECRET")


class SignUpView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SignUpForm()
        
        return render(request,"shop/signup.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SignUpForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            messages.success(request,"Account Created Successfully")
            
            return redirect("sign-in")
        
        messages.error(request,"Invalid Input")
        
        return render(request,"shop/signup.html",{"form":form_instance})
    
class SignInView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SignInForm()
        
        return render(request,"shop/signin.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SignInForm(request.POST)
        
        if form_instance.is_valid():
            
            data=form_instance.cleaned_data
            
            user_obj=authenticate(request,**data)
            
            if user_obj:
                
                login(request,user_obj)
                
                return redirect("index")
            
            messages.error(request,"Incorrect Username or Password")
            
            return render(request,"shop/signin.html",{"form":form_instance})
 
@method_decorator(signin_required,name="dispatch")
            
class IndexView(View):
    
    template_name="shop/index.html"
    
    def get(self,request,*args, **kwargs):
        
        qs=Product.objects.all().exclude(owner=request.user)
        
        types=Type.objects.all()
        
        return render(request,self.template_name,{"products":qs,"types":types})
    
    def post(self, request, *args, **kwargs):
        
        selected_type_id = request.POST.get('type')  # Get the selected type from the form
        
        types = Type.objects.all()  # Fetch all types for the dropdown again
        
        if selected_type_id=='all':
            
            products=Product.objects.all()
            
        else:

            products = Product.objects.filter(type_object__id=selected_type_id)

        return render(request, "shop/index.html", {"types": types, "products": products})
    
 
@method_decorator(signin_required,name="dispatch")
    
class UserProfileUpdateView(UpdateView):
    
    model=UserProfile
    
    form_class=UserProfileForm
    
    template_name="shop/userprofile_edit.html"
    
    success_url=reverse_lazy("index")

    

@method_decorator(admin_permission_required,name="dispatch")

class ProductCreateView(CreateView):
    
    model=Product
    
    form_class=ProductForm
    
    template_name="shop/product_add.html"
    
    success_url=reverse_lazy("index")
    
    def get(self,request,*args, **kwargs):
        
        form_instance=ProductForm()
        
        formset=ProductVariantFormSet()
        
        return render(request,self.template_name,{"form":form_instance,"formset":formset})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=ProductForm(request.POST,files=request.FILES)
        
        formset=ProductVariantFormSet(request.POST,files=request.FILES)
        
        if form_instance.is_valid() and formset.is_valid(): 
            
            product=form_instance.save(commit=False)   #creates a product instance but doesn’t save it to the database yet.
            
            product.owner=request.user
            
            product.save()
            
            form_instance.save_m2m()
            
            variants=formset.save(commit=False)
            
            for v in variants:
                
                v.product_object=product
                
                v.save()
                
            formset.save_m2m()
                
            return redirect(self.success_url)
  
        return render(request,self.template_name,{"form":form_instance,"formset":formset})
          

@method_decorator(admin_permission_required,name="dispatch")
class ProductUpdateView(UpdateView):
    
    model = Product
    
    form_class = ProductForm
    
    template_name = "shop/product_edit.html"
    
    success_url = reverse_lazy("index")
    
    def get(self, request, *args, **kwargs):
        
        id=kwargs.get("pk")
        
        product_object=Product.objects.get(id=id)
        
        form_instance = self.form_class(instance=product_object)
        
        formset = ProductVariantFormSet(instance=product_object)
        
        return render(request, self.template_name, {"form": form_instance, "formset": formset})
    
    def post(self, request, *args, **kwargs):
        
        id=kwargs.get("pk")
        
        product_object=Product.objects.get(id=id)
        
        form_instance = self.form_class(request.POST, files=request.FILES, instance=product_object)
        
        formset = ProductVariantFormSet(request.POST, files=request.FILES, instance=product_object)
        
        if form_instance.is_valid() and formset.is_valid():
            
            product = form_instance.save(commit=False)
            
            product.owner = request.user
            
            product.save()
            
            form_instance.save_m2m()
            
            variants = formset.save(commit=False)
            
            for v in variants:
                
                v.product_object = product
                
                v.save()
                
            formset.save_m2m()
            
            return redirect(self.success_url)
        
        return render(request, self.template_name, {"form": form_instance, "formset": formset})


@method_decorator(admin_permission_required,name="dispatch")
       
class MyProductListView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=request.user.products.all()
        
        return render(request,"shop/myproducts.html",{"items":qs})


@method_decorator(signin_required,name="dispatch")
    
class MyProductDeleteView(View):
    
     def get(self,request,*args, **kwargs):
         
         id=kwargs.get("pk")
         
         Product.objects.get(id=id).delete()
         
         return redirect("myproduct")
    

@method_decorator(signin_required, name="dispatch")
class ProductDetailView(View):
    
    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        product = Product.objects.get(id=id)

        return render(request, "shop/product_detail.html", {"product": product})


    def post(self, request, *args, **kwargs):

        product_id = kwargs.get("pk")

        product = Product.objects.get(id=product_id)

        size_id = request.POST.get("size_id")
  
        # Get the selected size object
        selected_size = Size.objects.filter(id=size_id).first()

        if not selected_size:

            messages.error(request, "Invalid size selected.")

            return redirect('product-detail', pk=product_id)

        
        # Get the available colors for the selected size
        colors = []

        price = None  # Initialize price variable

        for variant in product.product_variants.all():

            if selected_size in variant.size_object.all():

                colors.extend(variant.colour_object.all())

                price = variant.price  # Fetch the price for the selected size variant

        
        return render(request, "shop/product_detail.html", {

            "product": product,

            "selected_size": selected_size,

            "colors": colors,

            "price": price,  # Pass the price to the template

        })


@method_decorator(signin_required, name="dispatch")
class AddToCartView(View):

    def post(self, request, *args, **kwargs):

        id = kwargs.get('product_id')

        product = Product.objects.filter(id=id).first()

        size_id = request.POST.get('size_id')

        color_id = request.POST.get('color_id')

        quantity = int(request.POST.get('quantity', 1))
        
        size = Size.objects.filter(id=size_id).first()

        color = Colour.objects.filter(id=color_id).first()

        if not size or not color:

            messages.error(request, "Please select both size and color.")

            return redirect('product-detail', product_id=id)


        cart, created = Cart.objects.get_or_create(owner=request.user, is_active=True)


        product_variant = ProductVariant.objects.filter(
            product_object=product,
            size_object=size,
            colour_object=color
        ).first()

        if product_variant:

            Cart_items.objects.create(
                product_variant_object=product_variant,
                size_object=size,
                colour_object=color,
                cart_object=cart,
                quantity=quantity,
                is_order_placed=False
            )
            return redirect('index')

        messages.error(request, "Product variant not found.")

        return redirect('product-detail', pk=id)


@method_decorator(signin_required,name="dispatch")

class MyCartItemView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=request.user.basket.basket_items.filter(is_order_placed=False)
        
        total=request.user.basket.cart_total
        
        return render(request,"shop/mycartitems.html",{"cartitems":qs,"total":total})



@method_decorator(signin_required,name="dispatch")

class MyCartItemsDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Cart_items.objects.get(id=id).delete()
        
        return redirect("mycartitems")


@method_decorator(signin_required,name="dispatch")

class AddressView(View):
    
    def get(self, request, *args, **kwargs):                                                                 

        form_instance = AddressForm()

        qs = AddressStore.objects.all()

        return render(request, "shop/address.html", {"form": form_instance, "address": qs})

    

    def post(self, request, *args, **kwargs):

        form_instance = AddressForm(request.POST)

        selected_address_id = request.POST.get('selected_address_id')

        if selected_address_id:

            # Populate the form with the selected address data

            selected_address = AddressStore.objects.get(id=selected_address_id)

            form_instance = AddressForm(initial={

                'name': selected_address.name,

                'phone': selected_address.phone,

                'email': selected_address.email,

                'pin': selected_address.pin,

                'delivery_address': selected_address.delivery_address,

            })

        # Handle form submission (order creation, etc.)

        elif form_instance.is_valid():

            form_instance.instance.user_object = request.user

            address_instance = form_instance.save()

            request.session['address_id'] = address_instance.id

            

            if form_instance.instance.payment_method == "cash_on_delivery":

                cart_items = request.user.basket.basket_items.filter(is_order_placed=False)

                order = Orders.objects.create(

                    user_object=request.user,

                    address_object=address_instance,

                    is_paid=False,

                    total=request.user.basket.cart_total

                )

                order.cart_items_object.set(cart_items)
                
                if order:
                    print("sending email")

                    customer_name = order.address_object.name
                    
                    recipient_email = order.address_object.email

                    product_names = []

                    for cart_item in order.cart_items_object.all():
                        
                        product_name = cart_item.product_variant_object.product_object.title
                        
                        product_names.append(product_name)

                    product_names_str = ", ".join(product_names)

                    total = sum(cart_item.item_total_price for cart_item in order.cart_items_object.all())
                    
                    client_number=order.address_object.phone
                    
                    message_thread=threading.Thread(target=sent_text_message, args=(customer_name, product_names_str, total,client_number))

                    email_thread = threading.Thread(target=sent_email_message, args=(customer_name, product_names_str, total,recipient_email))
                    
                    email_thread.start()
                    
                    message_thread.start()

                    

                for ci in cart_items:

                    ci.is_order_placed = True

                    ci.save()
                    

                return render(request, "shop/cash_on_delivery.html", {"order": order})

            

            return redirect("online-payment")

        # Render the template with form errors or pre-filled form

        qs = AddressStore.objects.all()

        return render(request, "shop/address.html", {"form": form_instance, "address": qs})


    
    
@method_decorator(signin_required,name="dispatch")
   
class CashOnDeliveryListView(View):
    
 def get(self,request,*args, **kwargs):
     
     return render(request,"shop/cash_on_delivery.html")
 


 
import razorpay

@method_decorator(signin_required,name="dispatch")

class CheckOutView(View):
    
    def get(self,request,*args, **kwargs):
        
        client = razorpay.Client(auth=(key_ID,key_SECRET))
        
        amount=request.user.basket.cart_total*100

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
        
        payment = client.order.create(data=data)
        
        address_id = request.session.get('address_id')
        
        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)
        
        address_obj=Address.objects.filter(id=address_id,user_object=request.user,is_active=True).first()
        
        orders_obj=Orders.objects.create(
            
                            user_object=request.user,
                            
                            order_id=payment.get("id"),
                            
                            address_object=address_obj,
                            
                            total=request.user.basket.cart_total
        )
        
        
        
        for ci in cart_items:
            
            orders_obj.cart_items_object.add(ci)
            
            orders_obj.save()
            
        if orders_obj:
                    print("sending email")

                    customer_name = orders_obj.address_object.name
                    
                    recipient_email = orders_obj.address_object.email

                    product_names = []

                    for cart_item in orders_obj.cart_items_object.all():
                        
                        product_name = cart_item.product_variant_object.product_object.title
                        
                        product_names.append(product_name)

                    product_names_str = ", ".join(product_names)

                    total = request.user.basket.cart_total
                    
                    client_number=orders_obj.address_object.phone

                    message_thread=threading.Thread(target=sent_text_message, args=(customer_name, product_names_str, total,client_number))

                    email_thread = threading.Thread(target=sent_email_message, args=(customer_name, product_names_str, total,recipient_email))
                    
                    email_thread.start()
                    
                    message_thread.start()
            
            
        context={
            "key":key_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id"),
            "name": address_obj.name,
            "phone": address_obj.phone,
            "email":address_obj.email,
            "pin":address_obj.pin,
            "delivery_address":address_obj.delivery_address,
            "address": address_obj,
        }
        
        return render(request,"shop/payment.html",context)
    

# # {
#    'razorpay_order_id': razorpay_order_id,
#    'razorpay_payment_id': razorpay_payment_id,
#    'razorpay_signature': razorpay_signature
# #    }


from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt,name="dispatch")
 
class PaymentVerificationView(View):
    
    def post(self,request,*args, **kwargs):
        
        client = razorpay.Client(auth=(key_ID, key_SECRET))
        
        order_object=Orders.objects.get(order_id=request.POST.get('razorpay_order_id'))
        
        login(request,order_object.user_object)
        
        try:
            client.utility.verify_payment_signature(request.POST)
            
            print("Payment successfull")
            
            order_id=request.POST.get('razorpay_order_id')
            
            Orders.objects.filter(order_id=order_id).update(is_paid=True)
            
            cart_items=request.user.basket.basket_items.filter(is_order_placed=False)
            
            for ci in cart_items:
                
                ci.is_order_placed=True
                
                ci.save()
            
        except:
            
            print("Payment Failed")

        return redirect("index")



@method_decorator(signin_required,name="dispatch")
    
class MyPurchaseView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=Orders.objects.filter(Q(user_object=request.user,is_paid=True) | Q(address_object__payment_method="cash_on_delivery",user_object=request.user)).order_by("-created_date")
        
        return render(request,"shop/myorder_summary.html",{"orders":qs})




@method_decorator(signin_required,name="dispatch")

class ReviewCreateView(FormView):
    
    template_name="shop/review.html"
    
    form_class=ReviewForm
    
    def post(self,request,*args, **kwargs):
        
        form_instance=ReviewForm(request.POST)
        
        id=kwargs.get("pk")
        
        product_obj=Product.objects.get(id=id)
        
        if form_instance.is_valid():
            
            form_instance.instance.user_object=request.user
            
            form_instance.instance.product_object=product_obj
            
            try:
            
                form_instance.save()
            
                messages.success(request,"Thanks For Your Feedback !")
            
                return redirect("myorders")
            
            except:
        
                messages.success(request,"You have already reviewed this product.")
                
                return redirect("myorders")
        
        return render(request,"shop/review.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
    
class AddressEditView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        address_obj=Address.objects.get(id=id)
        
        form_instance=AddressForm(instance=address_obj)
        
        form_instance.fields['payment_method'].widget = forms.HiddenInput()
        
        return render(request,"shop/address_edit.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        address_obj=Address.objects.get(id=id)
        
        form_instance=AddressForm(request.POST,instance=address_obj)
        
        payment_method = address_obj.payment_method
        
        if form_instance.is_valid():
            
            form_instance.instance.payment_method=payment_method
            
            form_instance.save()
            
            return redirect("online-payment")
        
        return render(request,"shop/address_edit.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
    
class ReviewListView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        product_obj=Product.objects.get(id=id)
        
        qs=Reviews.objects.filter(product_object=product_obj)
        
        return render(request,"shop/review_list.html",{"reviews":qs})



@method_decorator(signin_required,name="dispatch")
    
class LogoutView(View):
    
    def get(self,request,*args, **kwargs):
        
        logout(request)
        
        messages.success(request,"Logout Successfull")
    
        return redirect("sign-in")
    
@method_decorator(signin_required,name="dispatch")
            
class MaterialCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=MaterialForm()
        
        return render(request,"shop/material_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=MaterialForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("material-all")
        
        return render(request,"shop/material_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
    
class MaterialUpdateView(UpdateView):
    
    model=Material
    
    form_class=MaterialForm
    
    template_name="shop/material_edit.html"
    
    success_url=reverse_lazy("material-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class MaterialListView(ListView):
    
    model=Material
    
    template_name="shop/material_list.html"
    
    context_object_name="materials"
    
@method_decorator(signin_required,name="dispatch")
    
class MaterialDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Material.objects.get(id=id).delete()
        
        return redirect("material-all")
    
    # Occasion
    
@method_decorator(signin_required,name="dispatch")
            
class OccasionCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=OccasionForm()
        
        return render(request,"shop/occasion_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=OccasionForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("occasion-all")
        
        return render(request,"shop/occasion_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
    
class OccasionUpdateView(UpdateView):
    
    model=Occasion
    
    form_class=OccasionForm
    
    template_name="shop/occasion_edit.html"
    
    success_url=reverse_lazy("occasion-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class OccasionListView(ListView):
    
    model=Occasion
    
    template_name="shop/occasion_list.html"
    
    context_object_name="occasions"
    
@method_decorator(signin_required,name="dispatch")
    
class OccasionDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Occasion.objects.get(id=id).delete()
        
        return redirect("occasion-all")
    
    # Colour
    
@method_decorator(signin_required,name="dispatch")
            
class ColourCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=ColourForm()
        
        return render(request,"shop/colour_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=ColourForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("colour-all")
        
        return render(request,"shop/colour_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
    
class ColourUpdateView(UpdateView):
    
    model=Colour
    
    form_class=ColourForm
    
    template_name="shop/colour_edit.html"
    
    success_url=reverse_lazy("colour-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class ColourListView(ListView):
    
    model=Colour
    
    template_name="shop/colour_list.html"
    
    context_object_name="colours"
    
@method_decorator(signin_required,name="dispatch")
    
class ColourDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Colour.objects.get(id=id).delete()
        
        return redirect("colour-all")
    
    # feature
    
@method_decorator(signin_required,name="dispatch")
            
class FeatureCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=FeatureForm()
        
        return render(request,"shop/feature_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=FeatureForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("feature-all")
        
        return render(request,"shop/feature_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
    
class FeatureUpdateView(UpdateView):
    
    model=Feature
    
    form_class=FeatureForm
    
    template_name="shop/feature_edit.html"
    
    success_url=reverse_lazy("feature-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class FeatureListView(ListView):
    
    model=Feature
    
    template_name="shop/feature_list.html"
    
    context_object_name="features"
    
@method_decorator(signin_required,name="dispatch")
    
class FeatureDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Feature.objects.get(id=id).delete()
        
        return redirect("feature-all")
    
    # type
    
@method_decorator(signin_required,name="dispatch")
            
class TypeCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=TypeForm()
        
        return render(request,"shop/type_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=TypeForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("type-all")
        
        return render(request,"shop/type_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
    
class TypeUpdateView(UpdateView):
    
    model=Type
    
    form_class=TypeForm
    
    template_name="shop/type_edit.html"
    
    success_url=reverse_lazy("type-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class TypeListView(ListView):
    
    model=Type
    
    template_name="shop/type_list.html"
    
    context_object_name="types"
    
@method_decorator(signin_required,name="dispatch")
    
class TypeDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Type.objects.get(id=id).delete()
        
        return redirect("type-all")
    
    # tag
    
@method_decorator(signin_required,name="dispatch")
            
class TagCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=TagForm()
        
        return render(request,"shop/tag_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=TagForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("tag-all")
        
        return render(request,"shop/tag_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
    
class TagUpdateView(UpdateView):
    
    model=Tag
    
    form_class=TagForm
    
    template_name="shop/tag_edit.html"
    
    success_url=reverse_lazy("tag-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class TagListView(ListView):
    
    model=Tag
    
    template_name="shop/tag_list.html"
    
    context_object_name="tags"
    
@method_decorator(signin_required,name="dispatch")
    
class TagDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Tag.objects.get(id=id).delete()
        
        return redirect("tag-all")
    
    # size
    
@method_decorator(signin_required,name="dispatch")
            
class SizeCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SizeForm()
        
        return render(request,"shop/size_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SizeForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("size-all")
        
        return render(request,"shop/size_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
    
class SizeUpdateView(UpdateView):
    
    model=Size
    
    form_class=SizeForm
    
    template_name="shop/size_edit.html"
    
    success_url=reverse_lazy("size-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class SizeListView(ListView):
    
    model=Size
    
    template_name="shop/size_list.html"
    
    context_object_name="sizes"
    
@method_decorator(signin_required,name="dispatch")
    
class SizeDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Size.objects.get(id=id).delete()
        
        return redirect("size-all")
    
    
@method_decorator(signin_required,name="dispatch")
    
class CashOndeliveryCancelView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        qs=Orders.objects.get(id=id,user_object=request.user)
        
        if not qs.is_paid:
            
            qs.is_canceled= True
            
            qs.canceled_at=timezone.now()
            
            qs.save()
        
        return redirect("myorders")


@method_decorator(admin_permission_required,name="dispatch")

class CashOnDeliveryOrderListView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=Orders.objects.filter(address_object__payment_method="cash_on_delivery",is_canceled=False,is_paid=False) 
        
        return render(request,"shop/codorderlist.html",{"orders":qs})
    
    
@method_decorator(admin_permission_required,name="dispatch")
    
class PaymentDoneView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        order=Orders.objects.get(id=id)
        
        order.is_paid=True
        
        order.save()
        
        return redirect("admin-order")
    
    
@method_decorator(signin_required,name="dispatch")    
class AddressCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=AddressAddForm()
        
        return render(request,"shop/address_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=AddressAddForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.instance.user_object=request.user
            
            form_instance.save()
            
            return redirect("address")
        
        return render(request,"shop/address_add.html",{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")    
class AddressStoreEditView(UpdateView):
    
    model=AddressStore
    
    form_class=AddressAddForm
    
    template_name="shop/address_store_edit.html"
    
    success_url=reverse_lazy("address")

@method_decorator(signin_required,name="dispatch")
class AddressStoreDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        AddressStore.objects.get(id=id).delete()
        
        return redirect("address")