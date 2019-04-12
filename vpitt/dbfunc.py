from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from accounts.models import User_profile
from timetable.models import Faculty, Group_info, Group
def get_user(request):
	try:
		user=User.objects.get(username = request.user)
		return(user)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_user_profile(username):   
	try:
		user = User_profile.objects.get(user__username = username)
		return(user)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_faculty():
	try:
		q = Faculty.objects.filter()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)


def get_groups_info():
	try:
		q = Group_info.objects.filter()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_group_info(id):
	try:
		q = Group_info.objects.filter(id  = id).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def create_group(kurs, id, subg):
	info = get_group_info(id)
	group = Group(curs = kurs, group_info = info, subgroup = subg) 
	group.save() 
	return group

def create_profile(user, group):
	print(group)
	user = User_profile(tt_json = "", user = user, group = group)
	user.save()