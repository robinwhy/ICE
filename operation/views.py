from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.groups.filter(name="instructor").exists():
        # user is an admin
        return redirect("instructors:list")
    else:
        return redirect("learners:usercenter")