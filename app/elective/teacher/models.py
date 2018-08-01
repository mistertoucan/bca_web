class Elective(object):

    def __init__(self, name, id):
        self.name = name
        self.id = id

class ElectiveTime(object):

    def __init__(self, time_id, day, mods):
        self.time_id = time_id
        self.days = day
        self.mods = mods