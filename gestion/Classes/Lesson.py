from Classes.Livings import Livings

class Lesson(Livings):

    def __init__(self, name):
        super(Lesson, self).__init__(name)
        self.schedule = self.create_Schedule()

    def print_my_schedule(self):
        print(self.schedule)

    def create_Schedule(self):
        # A raison de 4*7+4 = 32 heures de cours
        hours_nbr = 4 * 7 + 4
        schedule = []
        for i in range(hours_nbr):
            schedule.append(0)
        return schedule
