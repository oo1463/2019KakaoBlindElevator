
# Status Constant
STOPPED, OPENED, UPWARD, DOWNWARD = 'STOPPED', 'OPENED', 'UPWARD', 'DOWNWARD'

# Command Constant
UP, DOWN, STOP, OPEN, ENTER, EXIT, CLOSE = 'UP', 'DOWN', 'STOP', 'OPEN', 'ENTER', 'EXIT', 'CLOSE'


class Elevator:
    def __init__(self, num_problem, e_id, floor, passengers, status):
        self.__id = e_id
        self.__floor = floor
        self.__num_problem = num_problem
        self.__passengers = passengers  # array of call
        self.__status = status

        self.__MAX_PASSENGER_COUNT = 8

        self.__highest_floor = 0

        self.__commands = []

        if num_problem == 0:
            self.__highest_floor = 5
        else:
            self.__highest_floor = 25

    def set_items(self, floor, passengers, status):
        self.__floor = floor
        self.__passengers = passengers
        self.__status = status

    def get_floor(self):
        return self.__floor

    def make_command(self, what_command, calls=None):
        # print(self.__id)
        command = {'elevator_id': self.__id, 'command': what_command}
        if what_command == ENTER or what_command == EXIT:
            command['call_ids'] = [call['id'] for call in calls]
        return command

    def elevator_stop(self):
        self.__commands.append(self.make_command(STOP))
        self.__status = STOPPED

    def elevator_open(self):
        self.__commands.append(self.make_command(OPEN))
        self.__status = OPENED

    def elevator_close(self):
        self.__commands.append(self.make_command(CLOSE))
        self.__status = STOPPED

    def elevator_exit(self, calls):
        self.__commands.append(self.make_command(EXIT, calls))
        for call in calls:
            if call in self.__passengers:
                self.__passengers.remove(call)

    def elevator_enter(self, calls):
        self.__commands.append(self.make_command(ENTER, calls))
        self.__passengers.extend(calls)

    def elevator_up(self):
        self.__commands.append(self.make_command(UP))
        self.__status = UPWARD

    def elevator_down(self):
        self.__commands.append(self.make_command(DOWN))
        self.__status = DOWNWARD

    def find_out_calls(self):
        out_calls = []
        for passenger in self.__passengers:
            if passenger['end'] == self.__floor:
                out_calls.append(passenger)

        for passenger in out_calls:
            self.__passengers.remove(passenger)

        return out_calls

    def get_out_calls(self):

        past_status = self.__status

        out_calls = self.find_out_calls()
        if len(out_calls) == 0:
            return

        if self.__status == UPWARD or self.__status == DOWNWARD:
            self.elevator_stop()
            self.elevator_open()
        elif self.__status == STOPPED:
            self.elevator_open()

        self.elevator_exit(out_calls)
        self.elevator_close()

        self.__status = past_status

    def get_now_passenger_count(self):
        return len(self.__passengers)

    def get_in_calls(self, calls):
        past_status = self.__status

        if self.__status == UPWARD or self.__status == DOWNWARD:
            self.elevator_stop()
            self.elevator_open()
        elif self.__status == STOPPED:
            self.elevator_open()

        self.elevator_enter(calls)
        self.elevator_close()

        self.__status = past_status

    def get_elevator_status(self):
        return self.__status

    def is_at_max_floor(self):
        return self.__floor == self.__highest_floor

    def is_at_first_floor(self):
        return self.__floor == 1

    def get_max_passenger_count(self):
        return self.__MAX_PASSENGER_COUNT

    def get_commands(self):
        return self.__commands

    def get_first_command(self):
        return self.__commands[0]

    def del_first_command(self):
        self.__commands.pop(0)
