from django.shortcuts import render,redirect

from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from vpitt.dbfunc import get_user, get_user_profile, \
                        get_faculty, get_list_groups_info, \
                        create_profile, create_group, \
                        set_timetable_to_db, get_lessons, \
                        get_korpus, get_groups_name, get_users_schedules,\
                        get_group_by_id
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
def schedule_list_view(request):
    schedule_list = get_users_schedules(request.user)
    context = {"schedules":schedule_list}
    return render(request, "timetable/schedules_list.html", context)

@login_required
@require_http_methods(["GET"])
def add_new_schedules(request):
    groups = get_list_groups_info()
    c = {"groups":groups}
    return render(request, "timetable/add_new_sch.html", c)

@login_required
@require_http_methods(["POST"])
def add_new_schedules_post(request):
    print()
    print(request.POST["name-group"])
    print(request.POST["name-kurs"])
    print(request.POST["name-semester"])
    print(request.POST["name-subgroup"])
    group = create_group(request.POST["name-group"], 
                         request.POST["name-kurs"], 
                         request.POST["name-semester"],
                         request.POST["name-subgroup"],
                         request.user)
    print( group)
    if group:
        return redirect("/schedule_list/")
    return redirect("/add-new-schedules")
    

@login_required
@require_http_methods(["GET"])
def edit_schedule(request, group_id):
    method_decorator(csrf_protect)
    group = get_group_by_id(group_id)
    if group and (group.user_create == request.user):
        context = {"tt_json": "", "lessons": generate_lessons_list(group), "korpus": generate_korpus_list(), "group" : group}

        if group.tt_json:
            context["tt_json"] = group.tt_json

        return render(request, "timetable/timediv.html", context)


@login_required
@require_http_methods(["GET"])
def timetable_done(request, group_id):
    set_timetable_to_db(group_id)
    return render(request, "timetable/timetable_done.html")





def generate_lessons_list(group):
    lessons = get_lessons(group)
    lesson_list = {0:"Выберете предмет"}
    for item in enumerate(lessons):
        lesson_list[item[0]+1] = item[1].lesson.name
    lesson_list = json.dumps(lesson_list, ensure_ascii=False)
    return lesson_list

def generate_korpus_list():
    korpus = get_korpus()
    korpus_list = {0:""}
    for item in enumerate(korpus):
        korpus_list[item[0]+1] = item[1].letter
    korpus_list = json.dumps(korpus_list, ensure_ascii=False)
    return korpus_list