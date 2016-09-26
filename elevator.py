elevators = list()
highestFloor = 0
numElevators = 0
k = 0
global solutions
solutions = []


class Elevator:
    pass


class Peter:
    pass

peter = Peter()


# open and parse file
def open_file():
    # open input file and parse the data
    r = open("elevatortest.txt", "r")
    for line in r:
        array = line.split(".")
        # go through the array and get the highest floor
        # number of elevators
        # each elevator and their data
        for entry in array:
            if "top" in entry:
                global highestFloor
                highestFloor = get_num(entry)
            elif "elevators" in entry:
                numElevators = get_num(entry)
            elif "elevator" in entry:
                make_elevator_from_string(entry)
    r.close()


# extract numbers from strings
def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))


def make_elevator_from_string(info):
    # create an elevator
    temp = Elevator()

    # get the data from the string
    removeElevatorString = info.replace("elevator", '')
    removeParensString1 = removeElevatorString.replace("(", '')
    stringWithCommas = removeParensString1.replace(")", '')
    array = stringWithCommas.split(",")

    # construct the elevators data
    temp.elevatorNum = int(array[0])
    temp.startFloor = int(array[1])
    temp.endFloor = int(array[2])
    temp.currentFloor = temp.startFloor
    # 1 is up, 0 is down
    temp.direction = 1

    # add it to the list of elevators
    elevators.append(temp)


def construct_candidates(a, k):
    candidates = []
    # find an elevator that is at peter's floor
    for i in range(0, len(elevators)):
        # if the elevator's top or bottom is where peter currently is
        if (a[k-1].endFloor is elevators[i].endFloor) | (a[k-1].endFloor is elevators[i].startFloor):
            if a[k-1].elevatorNum is not elevators[i].elevatorNum:
                candidates.append(elevators[i])

    return candidates


def move_elevators():
    for i in range(0, len(elevators)):
        if elevators[i].currentFloor is elevators[i].endFloor:
            elevators[i].direction = 0
        elif elevators[i].currentFloor is elevators[i].startFloor:
            elevators[i].direction = 1

        if elevators[i].direction is 1:
            elevators[i].currentFloor += 1
        elif elevators[i].direction is 0:
            elevators[i].currentFloor -= 1


def make_move(a, k, currentFloor):
    timetaken = 0
    # waiting for the elevator
    while a[k].currentFloor is not currentFloor:
        move_elevators()
        timetaken += 1

    # move elevator to the top
    x = a[k].endFloor - a[k].currentFloor

    for i in range(x):
        move_elevators()
        timetaken += 1

    return timetaken


def unmake_move(timetaken):
    for i in range(0, timetaken):
        move_elevators()
    for i in range(0, len(elevators)):
        x = elevators[i].endFloor - elevators[i].startFloor
        if x % 2 is 1:
            if elevators[i].direction is 1:
                elevators[i].direction = 0
            else:
                elevators[i].direction = 1


def is_a_solution(a, k):
    if a[k].currentFloor is highestFloor:
        return True


def backtrack(a, k, timepassed):
    global solutions
    # if the current elevator we are on goes to the top
    if is_a_solution(a, k):
        if timepassed not in solutions:
            solutions.append(timepassed)
    # no? then get on another elevator
    else:
        k += 1
        c = construct_candidates(a, k)
        for i in range(0, len(c)):
            a.insert(k, c[i])
            currentFloor = a[k-1].currentFloor
            timetaken = make_move(a, k, currentFloor)
            timepassed += timetaken
            backtrack(a, k, timepassed)
            unmake_move(timetaken)
            a.pop(k)
            timepassed -= timetaken


def main():
    open_file()
    # initial set up
    # peter on 0th floor, no time passed
    peter.currentFloor = 0
    peter.elevatorNum = 0
    k = 0
    timepassed = 0
    a = []

    # peter isn't on an elevator the first time
    for i in range(0, len(elevators)):
        # if the elevator is currently at peter's floor
        if elevators[i].startFloor is 0:
            a.insert(0, elevators[i])
            x = a[0].endFloor - a[0].startFloor
            for i in range(x):
                move_elevators()
                timepassed += 1
            # start the backtracking
            backtrack(a, k, timepassed)

    global solutions
    print("min_time(", min(solutions), ").")


main()
