
class Livings:

    def __init__(self, name):
        self.name = name

    def create_Schedule(self):
        # A raison de 4*7+4 = 32 heures de cours
        hours_nbr = 4 * 7 + 4
        schedule = []
        for i in range(hours_nbr):
            schedule.append(0)
        return schedule
