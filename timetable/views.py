from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from vpitt.dbfunc import get_user, get_user_profile, get_faculty, get_groups_info, create_profile, create_group
# Create your views here.
# <QueryDict: {'csrfmiddlewaretoken': ['LG85ijmGsi7TbtEwcNydvh5B7qPsiRYocistWJVffO0vk1Xe93crXhQippVCafAD'], 
# 'name-faculty': ['1'], 
# 'name-kurs': ['3'], 
# 'name-group': ['5']}>


@login_required
def base_view(request):
    return render(request, "welcome.html")


@login_required
@require_http_methods(["GET"])
def fill_profile(request):
    faculty = get_faculty()
    groups = get_groups_info()
    c = {"faculty":faculty, "groups":groups}
    return render(request, "timetable/profile.html", c)

@login_required
@require_http_methods(["POST"])
def fill_profile_post(request):
    user_profile = get_user_profile(request.user)
    if not(user_profile):
        group = create_group(request.POST["name-kurs"], request.POST["name-group"], request.POST["name-subgroup"])
        create_profile(get_user(request), group)
    print("==========", request.POST["name-kurs"])
    return redirect("/fill_profile/")

@login_required
@require_http_methods(["GET"])
def table_view(request):
    user_profile = get_user_profile(request.user)
    if not(user_profile):
        return redirect("/fill_profile")

    method_decorator(csrf_protect)
    context = {"tt_json": ""}
    if user_profile.tt_json:
        context["tt_json"] = user_profile.tt_json
    
    return render(request, "timetable/timediv.html", context)


@login_required
@require_http_methods(["POST"])
def post(request):
    from ast import literal_eval
    var = literal_eval(list(request.POST.keys())[0])
    json_from_user = var["0"]
    user_profile = get_user_profile(request.user)
    user_profile.tt_json = json_from_user
    user_profile.save()
    print(json_from_user["second"])
    return HttpResponse(200)

