import json
import matplotlib.pyplot as plt
import mplcursors

grades = {'A': 10, 'A-': 9, 'B': 8, 'B-': 7,
          'C': 6, 'C-': 5, 'D': 4, 'E': 2, 'F': 0}


def add_semester():
    semester = {}
    semester['semester'] = input("Enter semester number: ")
    semester['no_of_courses'] = input("Enter number of courses: ")
    semester['courses'] = []
    for i in range(int(semester['no_of_courses'])):
        course = {}
        course['name'] = input("Enter course name: ")
        course['credits'] = float(input(f"Enter {course['name']} credits: "))
        course['grade'] = input(f"Enter {course['name']} grade: ")
        semester['courses'].append(course)
    semester['gpa'] = calculate_sgpa(semester['courses'])
    try:
        with open('semester_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    data.append(semester)

    # Sort data by semester number
    data.sort(key=lambda x: int(x["semester"]))

    with open('semester_data.json', 'w') as file:
        json.dump(data, file, indent=2)


def modify_semester():
    mod_sem = input("Enter semester number to modify: ")
    with open('semester_data.json', 'r') as file:
        data = json.load(file)

    index_to_modify = None
    for i, semester_data in enumerate(data):
        if semester_data["semester"] == mod_sem:
            index_to_modify = i
            break

    if index_to_modify is None:
        print("Semester not found")
        return
    else:
        num_courses = input("Enter number of courses: ")
        courses = []
        for i in range(int(num_courses)):
            course = {}
            course['name'] = input("Enter course name: ")
            course['credits'] = input(f"Enter {course['name']} credits: ")
            course['grade'] = input(f"Enter {course['name']} grade: ")
            courses.append(course)
        sgpa = calculate_sgpa(courses)
        data[index_to_modify]["courses"] = courses
        data[index_to_modify]["gpa"] = sgpa

    with open('semester_data.json', 'w') as file:
        json.dump(data, file, indent=2)


def calculate_sgpa(courses):

    total_credits = 0
    total_grade = 0
    for course in courses:
        total_credits += float(course['credits'])
        if course['grade'].isnumeric():
            total_grade += int(course['grade']) * \
                float(course['credits'])
        else:
            total_grade += float(course['credits']) * \
                grades[course['grade']]
    if total_credits == 0:
        return 0.0
    return total_grade / total_credits


def calculate_gpas():
    with open('semester_data.json', 'r') as file:
        data = json.load(file)
    for semester_data in data:
        # print(semester_data)
        courses = semester_data["courses"]
        semester_data["gpa"] = calculate_sgpa(courses)

    with open('semester_data.json', 'w') as file:
        json.dump(data, file, indent=2)


def get_cgpa():
    calculate_gpas()
    with open('semester_data.json', 'r') as file:
        semester_data = json.load(file)
    total_weighted_gpa = 0
    total_credits = 0

    for semester in semester_data:
        semester_gpa = semester.get("gpa", 0.0)
        total_weighted_gpa += semester_gpa * \
            sum(course["credits"] for course in semester.get("courses", []))
        total_credits += sum(course["credits"]
                             for course in semester.get("courses", []))

    if total_credits == 0:
        return 0.0
    else:
        print(total_weighted_gpa, total_credits)
        return total_weighted_gpa / total_credits


def calculate_cgpa(semester_data):
    # Calculate CGPA for all semesters
    total_weighted_gpa = 0
    total_credits = 0
    calculate_gpas()

    for semester in semester_data:
        semester_gpa = semester.get("gpa", 0.0)
        total_weighted_gpa += semester_gpa * \
            sum(course["credits"] for course in semester.get("courses", []))
        total_credits += sum(course["credits"]
                             for course in semester.get("courses", []))

    if total_credits == 0:
        return 0.0
    else:
        return total_weighted_gpa / total_credits


def plot_sg_cg():
    calculate_gpas()
    with open('semester_data.json', 'r') as file:
        data = json.load(file)
    max_semester = max(int(semester["semester"]) for semester in data)
    gpa_values = [semester.get("gpa", 0.0) for semester in data]
    cgpa_values = [calculate_cgpa(data[:semester_number])
                   for semester_number in range(1, max_semester + 1)]
    # Plotting
    plt.figure(figsize=(max_semester*1.5, 6))
    plt.plot(range(1, max_semester + 1), cgpa_values,
             marker='o', linestyle='-', color='b', label='CGPA')
    plt.plot(range(1, max_semester + 1), gpa_values,
             marker='o', linestyle='-', color='g', label='SGPA')
    # Set x-axis ticks at a difference of 1
    plt.xticks(range(1, max_semester + 1))
    plt.ylim(0, 10)  # Set y-axis range from 0 to 10
    plt.xlabel('Semester')
    plt.ylabel('Cumulative Grade Point Average (CGPA)')
    plt.title('CGPA Over Semesters')
    plt.legend()
    plt.grid(True)

    # Use mplcursors to display values on hover
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"{sel.target[1]:.2f}"))

    plt.show()


def gpa_for_cgpa(dgpa, credits):
    # get total credits from json
    calculate_gpas()
    with open('semester_data.json', 'r') as file:
        semester_data = json.load(file)
    total_weighted_gpa = 0
    total_credits = 0

    for semester in semester_data:
        semester_gpa = semester.get("gpa", 0.0)
        total_weighted_gpa += semester_gpa * \
            sum(course["credits"] for course in semester.get("courses", []))
        total_credits += sum(course["credits"]
                             for course in semester.get("courses", []))
    total = dgpa * (credits + total_credits)
    # print(total, total_weighted_gpa, credits)
    print((total - total_weighted_gpa) / credits)
    return (total - total_weighted_gpa) / credits


def expected_cgpa(dgpa, credits):
    # get total credits from json
    calculate_gpas()
    with open('semester_data.json', 'r') as file:
        semester_data = json.load(file)
    total_weighted_gpa = 0
    total_credits = 0

    for semester in semester_data:
        semester_gpa = semester.get("gpa", 0.0)
        total_weighted_gpa += semester_gpa * \
            sum(course["credits"] for course in semester.get("courses", []))
        total_credits += sum(course["credits"]
                             for course in semester.get("courses", []))
    total = total_weighted_gpa + (dgpa * credits)
    print(total / (credits + total_credits))
    return total / (credits + total_credits)


# add_semester()
# calculate_gpas()
# modify_semester()
# modify_credits()
# print(calculate_cgpa())
# plot_sg_cg()
