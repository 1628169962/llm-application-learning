import json
def load_students(name):
    with open(name,"r",encoding="utf-8") as f:
        students = json.load(f)
    return students
def filter_students(students):
    excellent_students = []
    for student in students:
        if student["score"] >= 90:
            excellent_students.append(student)
    excellent_students = sorted(excellent_students,key=lambda x:x["score"],reverse=True)
    return excellent_students

def save_students(excellent_students,position):
    with open(position,"w",encoding="utf-8") as f:
        json.dump(excellent_students,f,ensure_ascii=False,indent=2)

students=load_students("students.json")
excellent_students=filter_students(students)
save_students(excellent_students,"excellent_students.json")