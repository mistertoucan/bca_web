class ElectiveSection(object):

    def __init__(self, id, elective, section_nbr, tri, course_year, is_full, room_nbr, teacher, is_enrolled):
        self.id = id

        self.elective = elective
        self.section_nbr = section_nbr

        self.tri = tri
        self.course_year = course_year

        self.is_full = is_full

        self.room_nbr = room_nbr

        self.times = []

        self.teacher = teacher
        self.is_enrolled = is_enrolled

    def __str__(self):
        return "\n<%s: %s, %s, %s, %s, %s %s, %s, %s/>" % (self.id, self.elective, self.section_nbr, self.tri, self.course_year, self.max, self.enrolled, self.room_nbr, ', '.join([str(x) for x in self.times]))

    def getTimes(self):
        s = ' '

        for i in range(len(self.times)):
            s += self.times[i].__str__()

            if i < len(self.times)-1:
                s += ', '
        return s