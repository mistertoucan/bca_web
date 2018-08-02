class Elective(object):

    def __init__(self, id, name, desc):
        self.name = name
        self.desc = desc
        self.id = id

class ElectiveSection(object):

    def __init__(self, id, elective, section_nbr, tri, course_year, max, time):
        self.id = id

        self.elective = elective
        self.section_nbr = section_nbr

        self.tri = tri
        self.course_year = course_year

        self.enrolled = enrolled
        self.max = max

        self.time = time


class ElectiveTime(object):

    def __init__(self, id, day, mods):
        self.id = id
        self.day = day
        self.mods = mods