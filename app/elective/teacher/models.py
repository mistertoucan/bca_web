class Elective(object):

    def __init__(self, id, name, desc):
        self.name = name
        self.desc = desc
        self.id = id

        self.sections = []

class ElectiveSection(object):

    def __init__(self, id, elective, section_nbr, tri, course_year, max, room_nbr):
        self.id = id

        self.elective = elective
        self.section_nbr = section_nbr

        self.tri = tri
        self.course_year = course_year

        self.max = max
        self.enrolled = 0

        self.room_nbr = room_nbr

        self.times = []


class ElectiveTime(object):

    def __init__(self, id, day, mods):
        self.id = id
        self.day = day
        self.mods = mods