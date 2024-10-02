from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from myfancy.models import UserProfile,Product,ProductVariant,Address,Reviews

from django.forms import inlineformset_factory


class SignUpForm(UserCreationForm):
    
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    class Meta:
        
        model=User
        
        fields=["username","email","password1","password2"]
        
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            
            "email":forms.EmailInput(attrs={"class":"form-control"})
        }
        
class SignInForm(forms.Form):
    
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        
        model=UserProfile
        
        fields=["pic","name","bio","phone","address"]
        
        widgets={
            "pic":forms.FileInput(attrs={"class":"w-full p-2 my-3 border"}),
            "name":forms.TextInput(attrs={"class":"w-full p-2 my-3"}),
            "bio":forms.TextInput(attrs={"class":"w-full p-2 my-3"}),
            "phone":forms.NumberInput(attrs={"class":"w-full p-2 my-3"}),
            "address":forms.TextInput(attrs={"class":"w-full p-2 my-3"}),
        }
        
class ProductForm(forms.ModelForm):
    
    class Meta:
        
        model=Product
        
        exclude=("owner","created_date","updated_date","is_active")
        
        widgets={
            "title":forms.TextInput(attrs={"class":"w-full border my-5 p-2"}),
            "description":forms.Textarea(attrs={"class":"w-full border my-5 p-2","rows":4}),
            "image":forms.FileInput(attrs={"class":"w-full border my-5 p-2"}),
            "material_object":forms.CheckboxSelectMultiple(attrs={"class":"w-1/4 border my-5 p-2"}),
            "occasion_object":forms.Select(attrs={"class":"w-full border my-5 p-2"}),
            "feature_object":forms.CheckboxSelectMultiple(attrs={"class":"w-1/4 border my-5 p-2"}),
            "type_object":forms.Select(attrs={"class":"w-full border my-5 p-2"}),
            "tag_object":forms.CheckboxSelectMultiple(attrs={"class":"w-1/4 border my-5 p-2"})
            }
        
class ProductVariantForm(forms.ModelForm):
    
    class Meta:
        
        model=ProductVariant
        
        exclude=("created_date","updated_date","is_active")
        
        widgets={
            "product_object":forms.Select(attrs={"class":"w-full border my-5 p-2"}),
            "colour_object":forms.CheckboxSelectMultiple(attrs={"class":"w-1/4 border my-5 p-2"}),
            "size_object":forms.CheckboxSelectMultiple(attrs={"class":"w-1/4 border my-5 p-2"}),
            "price":forms.NumberInput(attrs={"class":"w-full border my-5 p-2"}),

        }
        
class AddressForm(forms.ModelForm):
    
    class Meta:
        
        model=Address
        
        fields=["name","phone","email","pin","delivery_address","payment_method"]
        
        widgets={
            "name":forms.TextInput(attrs={"class":"w-full border my-3 p-2"}),
            "phone":forms.NumberInput(attrs={"class":"w-full border my-3 p-2"}),
            "email":forms.EmailInput(attrs={"class":"w-full border my-3 p-2"}),
            "pin":forms.NumberInput(attrs={"class":"w-full border my-3 p-2"}),
            "delivery_address":forms.Textarea(attrs={"class":"w-full border my-3 p-2"}),
            "payment_method":forms.Select(attrs={"class":"w-full border my-3 p-2"}),
        }
        
class ReviewForm(forms.ModelForm):
    
    class Meta:
        
        model=Reviews
        
        fields=["comment","rating"]
        
        widgets={
            "comment":forms.Textarea(attrs={"class":"w-full border my-3 p-2"}),
            "rating":forms.NumberInput(attrs={"class":"w-full border my-3 p-2"})
        }

