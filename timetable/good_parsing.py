from models import Group_info, Lessons, Lessons_for_group

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
for n in namelist:
	file = open(name.format(n), 'r')
	for line in file:
		elem = line.split(";")
		if elem[0].lower() == "курс":
			print(elem[2].split(" "))
			# group_info = get_group_info(elem[])
			
