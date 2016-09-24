elevators = list()
highestFloor = 0
numElevators = 0
finished = False
k = 0
global solutions
solutions = []
global oldElevators
oldElevators = []


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


def move_elevators():
    global a
    for i in range(0, len(elevators)):
        if elevators[i].elevatorNum is not a[k].elevatorNum:
            if elevators[i].currentFloor is highestFloor:
                elevators[i].direction = 0
            elif elevators[i].currentFloor is elevators[i].endFloor:
                elevators[i].direction = 0
            elif elevators[i].currentFloor is elevators[i].startFloor:
                elevators[i].direction = 1

            if elevators[i].direction is 1:
                elevators[i].currentFloor += 1
            elif elevators[i].direction is 0:
                elevators[i].currentFloor -= 1


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


def construct_candidates(a, k, timepassed):
    global oldElevators
    candidates = []
    # peter isn't on an elevator the first time
    if len(a) is 0:
        for i in range(0, len(elevators)):
            # if the elevator is currently at peter's floor
            if elevators[i].currentFloor is 0:
                candidates.append(elevators[i])

    else:
        # find an elevator that is at peter's floor
        for i in range(0, len(elevators)):
            # if the elevator's top or bottom is where peter currently is
            if (a[k].currentFloor is elevators[i].endFloor) | (a[k].currentFloor is elevators[i].startFloor):
                if a[k].elevatorNum is not elevators[i].elevatorNum:
                    candidates.append(elevators[i])

    return candidates


def make_move(a, k, timepassed):
    # move the elevator we are on to it's end floor
    a[k].currentFloor = a[k].endFloor
    timepassed += a[k].endFloor - a[k].startFloor

    # move all the elevators this much, except the one we are on
    for i in range(0, timepassed):
        for j in range(0, len(elevators)):
            if elevators[j].elevatorNum is not a[k].elevatorNum:
                if elevators[j].currentFloor is elevators[j].endFloor:
                    elevators[j].direction = 0
                elif elevators[j].currentFloor is elevators[j].startFloor:
                    elevators[j].direction = 1

                if elevators[j].direction is 1:
                    elevators[j].currentFloor += 1
                elif elevators[j].direction is 0:
                    elevators[j].currentFloor -= 1
    return timepassed


def unmake_move(a, k, timepassed):
    for i in range(0, timepassed):
        if a[k].currentFloor is a[k].endFloor:
            a[k].currentFloor -= 1
            a[k].direction = 0
        elif a[k].currentFloor is a[k].startFloor:
            a[k].currentFloor += 1
            a[k].direction = 1
        elif a[k].direction is 0:
            a[k].currentFloor -= 1
        elif a[k].direction is 1:
            a[k].currentFloor += 1

    for i in range(0, timepassed):
        for j in range(0, len(elevators)):
            if elevators[j].currentFloor is elevators[j].endFloor:
                elevators[j].direction = 0
            elif elevators[j].currentFloor is elevators[j].startFloor:
                elevators[j].direction = 1

            if elevators[j].direction is 1:
                elevators[j].currentFloor += 1
            elif elevators[j].direction is 0:
                elevators[j].currentFloor -= 1


def is_a_solution(a, k):
    if len(a) is 0:
        return False
    if a[k].endFloor is highestFloor:
        return True


def backtrack(a, k, timepassed):
    c = []  # candidates for next move
    global solutions
    # if the current elevator we are on goes to the top
    if is_a_solution(a, k):
        solutions.append(timepassed + (a[k].currentFloor - a[k].endFloor))
    # no? then get on another elevator
    else:
        if len(a) > 1:
            k += 1
        else:
            k = 0
        c = construct_candidates(a, k, timepassed)
        for i in range(0, len(c)):
            a[i] = c[i]
            make_move(a, k, timepassed)
            backtrack(a, k, timepassed)
            unmake_move(a, k, timepassed)
            if finished:
                break

    return timepassed


def main():
    open_file()

    # initial set up
    # peter on 0th floor, no time passed
    peter.currentFloor = 0
    peter.elevatorNum = 0
    finished = False
    k = 0
    timepassed = 0
    a = []

    # start the backtracking
    backtrack(a, k, timepassed)

    global solutions
    print("time(", min(solutions), ")")


main()
