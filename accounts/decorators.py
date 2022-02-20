#Konrad Maciejczyk, 2021-2022
from django.shortcuts import redirect

def is_staff_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_side-home')

    return wrapper_func

def is_normal_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff == False:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_side-home')

    return wrapper_func
