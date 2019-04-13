from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from vpitt.dbfunc import get_user, get_user_profile, \
                        get_faculty, get_groups_info, \
                        create_profile, create_group, \
                        set_timetable_to_db, get_lessons, \
                        get_lesson_by_name, get_teacher_by_caf
import json
from ast import literal_eval
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
    user_profile = get_user_profile(request.user)
    if user_profile:
        return redirect("/timetable/")
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
    return redirect("/timetable/")

@login_required
@require_http_methods(["GET"])
def table_view(request):
    user_profile = get_user_profile(request.user)
    if not(user_profile):
        return redirect("/fill_profile")
    print(user_profile.group.group_info.cathedra)
    lessons = get_lessons()
    lesson_list = {0:"Выберете предмет"}

    for item in enumerate(lessons):
        lesson_list[item[0]+1] = item[1].name
    lesson_list = json.dumps(lesson_list, ensure_ascii=False)

    method_decorator(csrf_protect)
    context = {"tt_json": "", "lessons": lesson_list}
    if user_profile.tt_json:
        context["tt_json"] = user_profile.tt_json
    return render(request, "timetable/timediv.html", context)


@login_required
@require_http_methods(["POST"])
def post(request):
    var = literal_eval(list(request.POST.keys())[0])
    json_from_user = var["0"]
    user_profile = get_user_profile(request.user)
    user_profile.tt_json = json_from_user
    user_profile.save()
    print(json_from_user["second"])
    return HttpResponse(200)

@login_required
@require_http_methods(["GET"])
def timetable_done(request):
    user_profile = get_user_profile(request.user)
    set_timetable_to_db(user_profile)
    return render(request, "timetable/timetable_done.html")

@login_required
@require_http_methods(["POST"])
def get_teacher(request):
    name = request.POST["name"]
    lesson = get_lesson_by_name(name)
    teachers = get_teacher_by_caf(lesson.cathedra)
    teachers_dict = {0:"Выберете преподавателя"}
    for item in enumerate(teachers):
        s = (item[1].last_name) + " " + item[1].first_name[:1] + ". " + item[1].patronymic[:1] + "."
        teachers_dict[item[0]+1] = s
    teachers_dict = json.dumps(teachers_dict, ensure_ascii=False)

    # var = literal_eval(list(request.POST.keys()))
    # json_from_user = var    
    print("=====================", lesson.cathedra)
    return HttpResponse(teachers_dict)