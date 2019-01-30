class Signup_Dates(object):

    def __init__(self, id, grade_lvl, start, end, course_year, tri_nbr):
        self.id = id

        self.grade_lvl = grade_lvl

        self.start = start

        self.end = end

        self.course_year = course_year

        self.tri_nbr = tri_nbr

    def __str__(self):
        return "\n%s, %s, %s, %s, %s, %s" % (self.id, self.grade_lvl, self.start, self.end, self.course_year, self.tri_nbr)