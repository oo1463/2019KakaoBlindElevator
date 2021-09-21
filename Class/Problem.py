from API.Api import Api
from Class.Elevator import Elevator


# Status Constant
STOPPED, OPENED, UPWARD, DOWNWARD = 'STOPPED', 'OPENED', 'UPWARD', 'DOWNWARD'

# Command Constant
UP, DOWN, STOP, OPEN, ENTER, EXIT, CLOSE = 'UP', 'DOWN', 'STOP', 'OPEN', 'ENTER', 'EXIT', 'CLOSE'


class Problem:
    def __init__(self, num_problem, num_of_elevators):
        start = Api.get_auth_token(num_problem, num_of_elevators)
        self.__auth_token = start['token']
        self.__num_of_elevators = num_of_elevators
        self.__num_problem = num_problem
        self.__highest_floor = 0
        self.get_highest_floor()

        self.__is_end = False
        self.__calls = []
        self.__elevators = []

        self.__used_call_num = [False for x in range(1000)]

        for i in range(num_of_elevators):
            self.__elevators.append(Elevator(num_problem, i, 0, [], 0))

        self.get_on_call()
        self.__commands = []

    def get_highest_floor(self):
        if self.__num_problem == 0:
            self.__highest_floor = 5
        else:
            self.__highest_floor = 25

    def get_on_call(self):
        res = Api.oncall(self.__auth_token)
        elevators = res['elevators']
        calls = res['calls']
        self.__is_end = res['is_end']

        self.refresh_elevators(elevators)
        self.refresh_calls(calls)

    def refresh_elevators(self, elevators):
        for elevator in elevators:
            calls = elevator['passengers']
            call_list = [call for call in calls]

            self.__elevators[elevator['id']].set_items(elevator['floor'], call_list, elevator['status'])

    def refresh_calls(self, calls):
        self.__calls = []
        for call in calls:
            self.__calls.append(call)

    def action(self):
        Api.action(self.__auth_token, self.__commands)

    def find_calls_in_floor(self, elevator):
        calls_in_floor = []
        # print("FFFFF " + str(self.__calls))
        for call in self.__calls:
            if call['start'] == elevator.get_floor() and not self.__used_call_num[call['id']]:
                calls_in_floor.append(call)
        return calls_in_floor

    def simulate(self):

        while self.__is_end is False:
            self.get_on_call()

            for elevator in self.__elevators:

                if len(elevator.get_commands()) == 0:
                    # out call 확인
                    elevator.get_out_calls()

                    # in call 확인
                    calls_in_floor = self.find_calls_in_floor(elevator)
                    if len(calls_in_floor) > 0:
                        count_acceptable_call = elevator.get_max_passenger_count() - elevator.get_now_passenger_count()

                        elevator.get_in_calls(calls_in_floor[:count_acceptable_call])
                        for call in calls_in_floor[:count_acceptable_call]:  # 엘리베이터에 태운 call 목록 삭제
                            self.__used_call_num[call['id']] = True

                    # upward or downward
                    if elevator.get_elevator_status() == UPWARD and elevator.is_at_max_floor():
                        elevator.elevator_stop()
                    elif elevator.get_elevator_status() == DOWNWARD and elevator.is_at_first_floor():
                        elevator.elevator_stop()
                    elif elevator.get_elevator_status() == STOPPED and elevator.is_at_first_floor():
                        elevator.elevator_up()
                    elif elevator.get_elevator_status() == STOPPED and elevator.is_at_max_floor():
                        elevator.elevator_down()
                    elif elevator.get_elevator_status() == UPWARD:
                        elevator.elevator_up()
                    elif elevator.get_elevator_status() == DOWNWARD:
                        elevator.elevator_down()

                # print(elevator.get_commands())
                if elevator.get_first_command()['command'] == 'ENTER' and len(elevator.get_first_command()['call_ids']) == 0:
                    elevator.del_first_command()
                self.__commands.append(elevator.get_first_command())
                elevator.del_first_command()

            print(self.__commands)
            # print()
            self.action()
            self.__commands.clear()
