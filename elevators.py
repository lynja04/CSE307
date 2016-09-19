elevators = list()
highestFloor = 0
numElevators = 0
finished = False


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


def tick(timepassed):
    move_elevators()
    timepassed += 1
    return timepassed


def check_peter():
    if peter.currentFloor is highestFloor:
        return True
    else:
        return False


def move_elevators():
    for i in range(0, len(elevators)):
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

    # move peter's elevator
    for i in range(0, len(elevators)):
        if peter.elevatorNum is elevators[i].elevatorNum:
            peter.currentFloor = elevators[i].currentFloor


def move_other_elevators():
    for i in range(0, len(elevators)):
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


def main():
    open_file()

    timepassed = 0
    peter.currentFloor = 0
    peter.elevatorNum = 0

    # put peter on elevator that starts on first floor
    for i in range(0, len(elevators)):
        if elevators[i].startFloor is 0:
            peter.currentFloor = 0
            peter.elevatorNum = elevators[i].elevatorNum

    print("Peter's on elevator", peter.elevatorNum)

    finished = False

    while not finished:
        timepassed = tick(timepassed)
        finished = check_peter()
        if finished:
            break
        # make peter wait for an elevator
        if elevators[peter.elevatorNum-1].currentFloor is elevators[peter.elevatorNum-1].endFloor:
            print("Peter is getting off elevator", peter.elevatorNum, "at floor", elevators[peter.elevatorNum-1].currentFloor)
            peter.elevatorNum = 0
            while peter.elevatorNum is 0:
                move_other_elevators()
                timepassed += 1
                for i in range(0, len(elevators)):
                    if (peter.currentFloor is elevators[i].currentFloor) & ((elevators[i].currentFloor is elevators[i].endFloor) | (elevators[i].currentFloor is elevators[i].startFloor)) & (peter.elevatorNum is not elevators[i].elevatorNum):
                        if elevators[i].endFloor is 10:
                            peter.currentFloor = elevators[i].currentFloor
                            peter.elevatorNum = elevators[i].elevatorNum
                            print("Peter's on elevator", peter.elevatorNum, "on floor", peter.currentFloor)
                            if peter.currentFloor is 10:
                                finished = True

    print("Peter's on elevator", peter.elevatorNum, "on floor", peter.currentFloor)
    print("time(", timepassed, ")")

main()
