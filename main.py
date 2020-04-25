#! python3
import bs4, requests, smtplib
from temp import grade

subjects = {
	"◎ 數學Ⅱ" : "math",
	"◎ 歷史Ⅱ" : "history",
	"◎ 地理Ⅱ" : "geo",
	"◎ 國語文Ⅱ" : "chinese",
	"◎ 英語文Ⅱ" : "english",
	"◎ 化學Ⅱ" : "chem",
	"◎ 生物Ⅱ" : "bio"
}
new_grade = dict()

##################################################
url = "https://skytek.dali.tc.edu.tw/skyweb/"

#Get page
s = requests.Session()

payload = {
	"txtid" : "",
	"txtpwd" : "",
	"check" : "confirm"
}

payload2 = {
	"fncid" : "010090",
	"std_id" : "",
	"local_ip" : "",
	"contant" : ""
}

s.post(url + "main.asp", data = payload)

s.get(url + "f_left.asp")
s.post(url + "fnc.asp", data = payload2)
result = s.get(url + "/stu/stu_result9.asp")

result.encoding = "utf-8"

##################################################

soup = bs4.BeautifulSoup(result.content.decode('utf-8'), "html.parser")

oldfile = open('temp.py', 'r', encoding = 'utf-8').read()

with open("test.html", "w", encoding = "utf-8") as f:
  	f.write(str(result.text))

cnt = 9999
element = ""
for td in soup.findAll('td'):

	if td.string in subjects:
		element = subjects[td.string]
		cnt = 0
		continue
		
	#subject 1 not read yet or first three values (they are not grades)
	if cnt != 4:
		cnt += 1
		continue

	if td.string == ' ':
		new_grade[element] = "-1"
	else:
		new_grade[element] = td.string
	cnt += 1
	
changed_subjects = []
for sub in subjects:
	print(new_grade[subjects[sub]])
	if new_grade[subjects[sub]] != grade[subjects[sub]]:
		changed_subjects.append(subjects[sub])

print("changed =", len(changed_subjects))

##################################################

change_log = ""
for changed_subject in changed_subjects:
	change_log += '*' + changed_subject + "* before = " + grade[changed_subject] + ", after = " + new_grade[changed_subject]+'\n'

with open("temp.py", "w") as f:
	f.write("grade = {\n")
	for sub in subjects:
		f.write("\""+subjects[sub]+"\" : \"" + new_grade[subjects[sub]] + "\",\n")
	f.write("}")

##################################################


if len(changed_subjects) > 0:
	conn = smtplib.SMTP('smtp.gmail.com', 587)
	conn.ehlo()
	conn.starttls()
	conn.login('youremail@gmail.com', 'code')
	conn.sendmail('youremail@gmail.com', 'youremail@gmail.com', 'Subject:Grades updated~\n\n' + change_log)
	conn.quit()

	print("email sent")

##################################################


print(change_log)
print("finish")
