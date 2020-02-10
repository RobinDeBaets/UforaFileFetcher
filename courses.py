from json import JSONDecodeError

from brightspace import BrightspaceAPI, lp_root

brightspace_api = BrightspaceAPI()


def get_course(course_id):
    try:
        return brightspace_api.get_session().get(f"{lp_root}/enrollments/myenrollments/{course_id}").json()
    except JSONDecodeError:
        print(f"Course {course_id} does not exist")

def get_courses():
    def is_valid_course(course):
        course_info = course["OrgUnit"]
        return course_info["Type"]["Id"] == 3 and "Sandbox" not in course_info["Name"]

    courses = list(
        filter(is_valid_course, brightspace_api.get_session().get(f"{lp_root}/enrollments/myenrollments/").json()["Items"]))
    # First show pinned courses, then real courses
    courses.sort(key=lambda course: (bool(course["PinDate"]), " - " in course["OrgUnit"]["Name"]), reverse=True)
    return courses


def print_courses():
    courses = get_courses()
    print(" ID        NAME")
    for course in courses:
        course_info = course["OrgUnit"]
        print(f""" {course_info["Id"]:>6}    {course_info["Name"]}""")
