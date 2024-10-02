from django.shortcuts import redirect,render

from django.contrib import messages

def signin_required(fn):
    
    def wrapper(request,*args, **kwargs):
        
        if not request.user.is_authenticated:
            
            messages.error(request,"Invalid Session Please LogIn")
            
            return redirect("sign-in")
        
        return fn(request,*args,**kwargs)
    
    return wrapper


def admin_permission_required(fn):
    
    def wrapper(request,*args,**kwargs):
        
        if request.user.is_superuser:
            
            return fn(request,*args, **kwargs)
        
        messages.error(request,"Only admin can access")
        
        return redirect("sign-in")
    
    return wrapper
    
    
