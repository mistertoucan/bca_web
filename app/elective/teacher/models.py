class Elective(object):

    def __init__(self, name, desc, id):
        self.name = name
        self.desc = desc
        self.id = id

class ElectiveTime(object):

    def __init__(self, time_id, day, mods):
        self.time_id = time_id
        self.day = day
        self.mods = mods