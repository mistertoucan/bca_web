class ElectiveSection(object):
    def __init__(self, id, elective
                 , section_nbr, tri, course_year, enrolled_count, max, room_nbr, teacher, times, is_student_enrolled):
        self.id = id

        self.elective = elective
        self.section_nbr = section_nbr

        self.tri = tri
        self.course_year = course_year

        self.enrolled_count = enrolled_count
        self.max = max

        self.room_nbr = room_nbr

        self.times = times

        self.teacher = teacher
        self.is_student_enrolled = is_student_enrolled

    def __str__(self):
        return "\n<%s: %s, %s, %s, %s, %s %s, %s, %s/>" % (self.id, self.elective, self.section_nbr, self.tri, self.course_year, self.max, self.enrolled, self.room_nbr, ', '.join([str(x) for x in self.times]))

    def getTimes(self):
        s = ' '

        for i in range(len(self.times)):
            s += self.times[i].__str__()

            if i < len(self.times)-1:
                s += ', '
        return s


class Elective(object):

    def __init__(self, id, name, desc, req):
        self.id = id
        self.name = name
        self.desc = desc
        self.prereq = req

    def __str__(self):
        return "<%s: %s, %s/>" % (self.id, self.name, self.desc)


class ElectiveTeacher(object):

    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

class EnrollmentTime(object):

    def __init__(self, grade_level, start_time, end_time, course_year, tri_nbr):
        self.grade_level = grade_level
        self.start_time = start_time
        self.end_time = end_time
        self.course_year = course_year
        self.tri_nbr = tri_nbr