from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from accounts.models import User_profile
from timetable.models import Faculty, Group_info, Group, Teacher, Lessons, Room, Korpus
from ast import literal_eval

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

def get_groups_name(user):
	group = get_user_profile(user.username).group
	name = str(group.group_info.abbr) + "-" + str(group.curs) + str(group.group_info.code)
	return name

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

def get_lessons():
	try:
		q = Lessons.objects.filter()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_lesson_by_name(name):
	try:
		q = Lessons.objects.filter(name = name).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)


def get_korpus_by_name(name):
	try:
		q = Korpus.objects.filter(letter = name).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_rooms_by_korpus(korpus):
	try:
		q = Room.objects.filter(korpus = korpus)
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_teacher_by_caf(cathedra):
	try:
		q = Teacher.objects.filter(cathedra = cathedra)
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

def get_korpus():
	try:
		q = Korpus.objects.filter()
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


class Lesson(object): 

	def __init__(self, lesson): 
		if not(bool(lesson) == False):
			self.name = lesson["name"]
			self.teach = lesson["teach"]
			self.korpus = lesson["korpus"]
			self.room = lesson["room"]
			self.type_lesson = lesson["type"] 

	# def check_lesson(self):
	# 	if get_lesson_by_name(self.name):
	# 		return True
	# 	else return False

	# def check_teach(self):
	# 	if get_teach_by_name(self.name):
	# 		return True
	# 	else return False

	# def check_korpus(self):
	# 	if get_korpus_by_name(self.name):
	# 		return True
	# 	else return False

	# def check_room(self):
	# 	if get_room_by_name(self.name):
	# 		return True
	# 	else return False

	# def check_type_lesson(self):
	# 	if get_type_lesson_by_name(self.name):
	# 		return True
	# 	else return False

	def __str__(self):
		try:
			return("\n         name: " + str(self.name) + 
				   "\n         teach: " + str(self.teach) + 
				   "\n         room: " + str(self.korpus) + "-"+ str(self.room) + 
				   "\n         type_lesson: " + str(self.type_lesson)
				  )
		except AttributeError as e:
			return("") 
			

	

class Day(object):

	def __init__(self,day):
		self.l1 = Lesson(day["l1"])
		self.l2 = Lesson(day["l2"])
		self.l3 = Lesson(day["l3"])
		self.l4 = Lesson(day["l4"])
		self.l5 = Lesson(day["l5"])
		self.l6 = Lesson(day["l6"])

	def __str__(self):
		return("\n      l1"+ str(self.l1) + 
			   "\n      l2"+ str(self.l2) +
			   "\n      l3"+ str(self.l3) +
			   "\n      l4"+ str(self.l4) +
			   "\n      l5"+ str(self.l5) +
			   "\n      l6"+ str(self.l6) 
			   )



class Week(object):

	def __init__(self, week):
		self.mon =  Day(week["mon"])
		self.tues =  Day(week["tues"])
		self.wen =  Day(week["wen"])
		self.thurs=  Day(week["thurs"])
		self.fri =  Day(week["fri"])
		self.sat =  Day(week["sat"])

	def __str__(self):
		return("\n   mon"+ str(self.mon) + 
			   "\n   tues"+ str(self.tues) +
			   "\n   wen"+ str(self.wen) +
			   "\n   thurs"+ str(self.thurs) +
			   "\n   fri"+ str(self.fri) +
			   "\n   sat"+ str(self.sat) 
			   )

class TimeTableFormJson(object):

	def __init__(self, timetable_dict):
		self.first = Week(timetable_dict["first"])
		self.second = Week(timetable_dict["second"])

	def __str__(self):
		return("\nfirst"+ str(self.first) + "\nsecond" + str(self.second))

def set_timetable_to_db(user_profile):
	timetable_dict = literal_eval(user_profile.tt_json)
	timetable = TimeTableFormJson(timetable_dict)
	print("==========================",timetable)



  #   group = models.ForeignKey("Group", on_delete=models.SET_NULL,  null = True)
  #   day = models.ForeignKey("DaysWeek", on_delete=models.SET_NULL,  null = True)
  #   number_week = models.IntegerField()
  #   lesson_time = models.ForeignKey("LessonTime", on_delete=models.SET_NULL,  null = True)
  #   lesson = models.ForeignKey("Lessons", on_delete=models.SET_NULL,  null = True)
  #   teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL,  null = True)
  #   room = models.ForeignKey("Room", on_delete=models.SET_NULL,  null = True)
  #   type_lessons = models.ForeignKey("TypeLesson", on_delete=models.SET_NULL,  null = True)