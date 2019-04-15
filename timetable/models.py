from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
	name = models.CharField(max_length = 100, null = True)
	abbr = models.CharField(max_length = 100)

class Cathedra(models.Model):
	name = models.CharField(max_length = 100)
	abbr = models.CharField(max_length = 100)
	faculty = models.ForeignKey("Faculty", on_delete=models.SET_NULL,  null = True)

class Korpus(models.Model):
    letter = models.CharField(max_length = 10)

class Group_info(models.Model):
	specialty = models.CharField(max_length = 100)
	abbr = models.CharField(max_length = 100)
	code = models.CharField(max_length = 100)
	course = models.IntegerField(default = 0)
	semester = models.IntegerField(default = 0)
	cathedra = models.ForeignKey("Cathedra", on_delete=models.SET_NULL,  null = True)
	
class Group(models.Model):
	group_info = models.ForeignKey("Group_info", on_delete=models.SET_NULL, null = True)
	subgroup = models.IntegerField()

class DaysWeek(models.Model):
    name = models.CharField(max_length = 20)

class LessonTime(models.Model):
    number_lesson = models.IntegerField()
    start = models.TimeField()
    end = models.TimeField()

class Room(models.Model):
    number = models.IntegerField()
    korpus = models.ForeignKey("Korpus", on_delete=models.SET_NULL, null = True)

class Lessons(models.Model):
    name = models.CharField(max_length = 100)
    short_name = models.CharField(max_length = 100)
    cathedra = models.ForeignKey("Cathedra", on_delete=models.SET_NULL,  null = True)

class TypeLesson(models.Model):
    name = models.CharField(max_length = 50)

class Lessons_for_group(models.Model):
	group_info = models.ForeignKey("Group_info", on_delete=models.SET_NULL,  null = True)
	lesson = models.ForeignKey("Lessons", on_delete=models.SET_NULL,  null = True)

class Teacher(models.Model):
    first_name = models.CharField(max_length = 100, null = True)
    last_name = models.CharField(max_length = 100)
    patronymic = models.CharField(max_length = 100, null = True)
    cathedra = models.ForeignKey("Cathedra", on_delete=models.SET_NULL,  null = True)

class Time_table(models.Model):
    group = models.ForeignKey("Group", on_delete=models.SET_NULL,  null = True)
    day = models.ForeignKey("DaysWeek", on_delete=models.SET_NULL,  null = True)
    number_week = models.IntegerField()
    lesson_time = models.ForeignKey("LessonTime", on_delete=models.SET_NULL,  null = True)
    lesson = models.ForeignKey("Lessons", on_delete=models.SET_NULL,  null = True)
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL,  null = True)
    room = models.ForeignKey("Room", on_delete=models.SET_NULL,  null = True)
    type_lessons = models.ForeignKey("TypeLesson", on_delete=models.SET_NULL,  null = True)

{1:'faculty',2:'cathedra',3:'korpus',4:'room',5:'daysweek',6:'typelesson', 7:'timelesson', 8:'teacher',9:'group', 10:'subject'}

s = "data/"

def faculty_fill():
	f = open(s + "faculty", "r")
	for line in f:
		l = list(line.split("|"))
		print(l)
		if len(Faculty.objects.filter(name = l[1].replace("\n", ""))) == 0:
			obj = Faculty(name = l[1].replace("\n", ""), abbr =l[0])
			obj.save()


def cathedra_fill():
	f = open(s + "cathedra", "r")
	facultet = Faculty()
	for line in f:
		if '@' in line:
			stri = line[1:].replace("\n", "")
			facultet = Faculty.objects.filter(abbr = stri)[0]
			print(facultet)
			continue
		l = list(line.split("|"))
		print(l)
		if len(Cathedra.objects.filter(name = l[0].replace("\n", ""))) == 0:
			obj = Cathedra(name = l[0].replace("\n", ""), abbr =l[1].replace("\n", ""), faculty = facultet)
			obj.save()


def korpus_fill():
	f = open(s + "korpus", "r")
	for line in f:
		l = list(line.split("|"))
		print(l)
		if len(Korpus.objects.filter(letter = l[0].replace("\n", ""))) == 0:
			obj = Korpus(letter = l[0].replace("\n", ""))
			obj.save()

def room_fill():
	f = open(s + "room", "r")
	krps = Korpus()
	for line in f:
		if '@' in line:
			stri = line[1:].replace("\n", "")
			krps = Korpus.objects.filter(letter = stri)[0]
			continue
		l = list(line.split("|"))
		print(l)
		if len(Room.objects.filter(number = l[0].replace("\n", ""))) == 0:
			obj = Room(number = l[0].replace("\n", ""), korpus = krps)
			obj.save()

def daysweek_fill():
	f = open(s + "daysweek", "r")
	for line in f:
		l = list(line.split("|"))
		print(l)
		if len(DaysWeek.objects.filter(name = l[0].replace("\n", ""))) == 0:
			obj = DaysWeek(name = l[0].replace("\n", ""))
			obj.save()

def typelesson_fill():
	f = open(s + "typelesson", "r")
	for line in f:
		l = list(line.split("|"))
		print(l)
		if len(TypeLesson.objects.filter(name = l[0].replace("\n", ""))) == 0:
			obj = TypeLesson(name = l[0].replace("\n", ""))
			obj.save()

def timelesson_fill():
	f = open(s + "timelesson", "r")
	for line in f:
		l = list(line.split("|"))
		print(l)
		if len(LessonTime.objects.filter(number_lesson = l[0].replace("\n", ""))) == 0:
			obj = LessonTime(number_lesson  = l[0].replace("\n", ""),
							 start  = l[1].replace("\n", ""),
							 end  = l[2].replace("\n", "")
							)
			obj.save()

def teacher_fill():
	f = open(s + "teacher", "r")
	caf = Cathedra()
	for line in f:
		if '@' in line:
			stri = line[1:].replace("\n", "")
			caf = Cathedra.objects.filter(abbr = stri)[0]
			continue
		l = list(line.split("|"))
		print(l)
		l = list(l[0].split(" "))
		if len(Teacher.objects.filter(last_name = l[0].replace("\n", ""))) == 0:
			obj = Teacher(first_name = l[1].replace("\n", ""),
						last_name  = l[0].replace("\n", ""),
						patronymic = l[2].replace("\n", ""),
						cathedra = caf
					    )
			obj.save()

def group_info_fill():
	f = open(s + "group", "r")
	caf = Cathedra()
	for line in f:
		if '@' in line:
			stri = line[1:].replace("\n", "")
			caf = Cathedra.objects.filter(abbr = stri)[0]
			print(caf)
			continue
		l = list(line.split("|"))
		print(l)
		if len(Group_info.objects.filter(code = l[2].replace("\n", ""))) == 0:
			for course in range(1,5):
				for semester in range(1,3):
					obj = Group_info(specialty = l[0].replace("\n", ""), 
									 abbr =l[1].replace("\n", ""),
									 code=l[2].replace("\n", ""), 
									 course = course,
									 semester = semester,
									 cathedra = caf)
					obj.save()

def subject_fill():
	f = open(s + "subject", "r")
	caf = Cathedra()
	for line in f:
		l = list(line.split("|"))
		print(l)
		caf = Cathedra.objects.filter(name = l[2].replace("\n", ""))[0]
		
		if len(Lessons.objects.filter(name = l[0].replace("\n", ""))) == 0:
			obj = Lessons(name = l[0].replace("\n", ""),
						  short_name  = l[1].replace("\n", ""),
						  cathedra = caf
					    )
			obj.save()



print("==========-----------=============--------------=============--------")
# faculty_fill()
# print()
# cathedra_fill()
# print()
# korpus_fill()
# print()
# room_fill()
# print()
# daysweek_fill()
# print()
# typelesson_fill()
# print()
# timelesson_fill()
# print()
# teacher_fill()
# print()
# group_info_fill()
# print()
# subject_fill()
print("==========---------DONE--==DONE=====DONE-------========--------")

number_arr = ["первый", "второй", "третий", "четвертый","пятый", "шестой", "седьмой", "восьмой"]
name = "data/dekan_data/{}.csv"
namelist = [
"ввт",
"вип",
"вхт",
"вэ",
"вэм"
]
# group = Group_info()
# lessons = Lessons()
f_dict = {}
kurs = int()
group_abbr = str()
sem = int()
for n in namelist:
	file = open(name.format(n), 'r')

	for line in file:
		line = line.replace("\n","")
		elem = line.split(";")
		if elem[0].lower() == "курс":
			ku = elem[1] 
			l = elem[2].split(" ")
			gr = l[len(l)-1].split("-")[0]
			print(ku, gr)
		if line.lower() in number_arr:
			sem = number_arr.index(line.lower())+1
			print(sem)
		print
		if elem[1].isdigit():
			print(elem[3])
			print()
			caf = Cathedra.objects.filter(abbr = elem[3]).get()
			lesson = Lesson(name = elem[2], cathedra = caf)
			lessno.save()

			# group_info = get_group_info(elem[])
			
