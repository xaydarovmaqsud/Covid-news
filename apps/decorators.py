from django.shortcuts import redirect

def not_logged(func):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return func(request,*args,**kwargs)
    return wrapper

def no_logged(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('new')
        return func(request,*args,**kwargs)
    return wrapper