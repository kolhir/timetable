from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# from accounts.models import User_profile
from timetable.models import Faculty, Group_info, TypeLesson ,Group, Teacher, Lessons, Room, Korpus, Lessons_for_group, Time_table, DaysWeek, LessonTime
from ast import literal_eval
import copy
#############################
from termcolor import cprint
def print_message(message):
	cprint(("!!!!! " + str(message) + " !!!!!"), 'red',attrs=['bold'])
#############################

def get_group_by_id(id):
	try:
		group = Group.objects.filter(id = id).get()
		return(group)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_users_schedules(user):
	try:
		groups = Group.objects.filter(user_create = user)
		return(groups)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)


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


def get_list_groups_info():
	try:
		q = Group_info.objects.filter(course = 1, semester = 1)
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_lessons(group):
	try:
		q = Lessons_for_group.objects.filter(group_info = group.group_info)

		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)


#################################
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

def get_teacher_by_name(name):
	try:
		q = Teacher.objects.filter(last_name = name).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_room_by_name(name, korpus):
	try:
		q = Room.objects.filter(number = name, korpus = korpus ).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_type_by_name(name):
	try:
		q = TypeLesson.objects.filter(name = name).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)
#################################


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

def get_group_info(abbr, course, semester):
	try:
		q = Group_info.objects.filter(abbr = abbr, course = course, semester = semester).get()
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

def create_group(abbr, course, sem ,subg, user):
	info = get_group_info(abbr, course, sem)
	print("!!!!!!!!!!!!!!", info)
	group = False
	if ((int(subg) in (1,2,0)) and info):

		group = Group( group_info = info, subgroup = subg, user_create = user) 
		group.save() 
	return group

def create_profile(user, group):
	print(group)
	user = User_profile(tt_json = "", user = user, group = group)
	user.save()




day_c = {"mon" : "Понедельник",
             "tues": "Вторник",
             "wen": "Среда",
             "thurs": "Четверг",
             "fri": "Пятница",
             "sat": "Суббота"
            }
            
def get_day_by_name(name):
	try:
		q = DaysWeek.objects.filter(name = day_c[name]).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

def get_lesson_time_by_name(n):
	try:
		q = LessonTime.objects.filter(number_lesson = n).get()
		return(q)
	except ObjectDoesNotExist:
		return(False)
	except  MultipleObjectsReturned:
		return(False)

class Lesson(object): 

	def __init__(self, lesson, schedule): 
		if not(bool(lesson) == False):
			self.name = lesson["name"]
			schedule.lesson = get_lesson_by_name(lesson["name"])
			self.teach = lesson["teach"]
			schedule.teacher = get_teacher_by_name(list(lesson["teach"].split(" "))[0])
			self.korpus = lesson["korpus"]
			schedule.korpus = get_korpus_by_name(lesson["korpus"])
			self.room = lesson["room"]
			schedule.room = get_room_by_name(lesson["room"], schedule.korpus)
			self.type_lessons = lesson["type"] 
			schedule.type_lessons = get_type_by_name(lesson["type"]) 
			schedule.save()

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

	def __init__(self,day, schedule):
	
		tt_1 = copy.deepcopy(schedule)
		tt_1.lesson_time = get_lesson_time_by_name(1)
		tt_2 = copy.deepcopy(schedule)
		tt_2.lesson_time = get_lesson_time_by_name(2)
		tt_3 = copy.deepcopy(schedule)
		tt_3.lesson_time = get_lesson_time_by_name(3)
		tt_4 = copy.deepcopy(schedule)
		tt_4.lesson_time = get_lesson_time_by_name(4)
		tt_5 = copy.deepcopy(schedule)
		tt_5.lesson_time = get_lesson_time_by_name(5)
		tt_6 = copy.deepcopy(schedule)
		tt_6.lesson_time = get_lesson_time_by_name(6)


		self.l1 = Lesson(day["l1"], tt_1)
		self.l2 = Lesson(day["l2"], tt_2)
		self.l3 = Lesson(day["l3"], tt_3)
		self.l4 = Lesson(day["l4"], tt_4)
		self.l5 = Lesson(day["l5"], tt_5)
		self.l6 = Lesson(day["l6"], tt_6)

	def __str__(self):
		return("\n      l1"+ str(self.l1) + 
			   "\n      l2"+ str(self.l2) +
			   "\n      l3"+ str(self.l3) +
			   "\n      l4"+ str(self.l4) +
			   "\n      l5"+ str(self.l5) +
			   "\n      l6"+ str(self.l6) 
			   )



class Week(object):

	def __init__(self, week, schedule):
		tt_mon = copy.deepcopy(schedule)
		tt_mon.day = get_day_by_name("mon")

		tt_tues = copy.deepcopy(schedule)
		tt_tues.day = get_day_by_name("tues")
		tt_wen = copy.deepcopy(schedule)
		tt_wen.day = get_day_by_name("wen")
		tt_thurs = copy.deepcopy(schedule)
		tt_thurs.day = get_day_by_name("thurs")
		tt_fri = copy.deepcopy(schedule)
		tt_fri.day = get_day_by_name("fri")
		tt_sat = copy.deepcopy(schedule)
		tt_sat.day = get_day_by_name("sat")


		self.mon =  Day(week["mon"],tt_mon)
		self.tues =  Day(week["tues"],tt_tues)
		self.wen =  Day(week["wen"],tt_wen)
		self.thurs=  Day(week["thurs"],tt_thurs)
		self.fri =  Day(week["fri"],tt_fri)
		self.sat =  Day(week["sat"],tt_sat)

	def __str__(self):
		return("\n   mon"+ str(self.mon) + 
			   "\n   tues"+ str(self.tues) +
			   "\n   wen"+ str(self.wen) +
			   "\n   thurs"+ str(self.thurs) +
			   "\n   fri"+ str(self.fri) +
			   "\n   sat"+ str(self.sat) 
			   )

class TimeTableFormJson(object):

	def __init__(self, timetable_dict, group, schedule):
		self.group = group
		schedule.group = group
		v1 =  copy.deepcopy(schedule)
		v1.number_week = 1
		v2 =  copy.deepcopy(schedule)
		v2.number_week = 2
		self.first = Week(timetable_dict["first"], v1)
		self.second = Week(timetable_dict["second"], v2)

	def __str__(self):
		return("\nfirst"+ str(self.first) + "\nsecond" + str(self.second))

def set_timetable_to_db(id):
	group = get_group_by_id(id)
	timetable_dict = literal_eval(group.tt_json)
	schedule = Time_table()
	timetable = TimeTableFormJson(timetable_dict, group, schedule)
	print("==========================",timetable)



  #   group = models.ForeignKey("Group", on_delete=models.SET_NULL,  null = True)
  #   day = models.ForeignKey("DaysWeek", on_delete=models.SET_NULL,  null = True)
  #   number_week = models.IntegerField()
  #   lesson_time = models.ForeignKey("LessonTime", on_delete=models.SET_NULL,  null = True)
  #   lesson = models.ForeignKey("Lessons", on_delete=models.SET_NULL,  null = True)
  #   teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL,  null = True)
  #   room = models.ForeignKey("Room", on_delete=models.SET_NULL,  null = True)
  #   type_lessons = models.ForeignKey("TypeLesson", on_delete=models.SET_NULL,  null = True)