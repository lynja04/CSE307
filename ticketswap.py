import sys
import itertools

class Passenger:
    pass


class Subway:
    pass

global solutions
solutions = []
passengers = list()
subway = Subway()

# open a file and make passengers
def openFile(fileName):
    # open input file and parse the data
    r = open(fileName, "r")
    for line in r:
        array = line.split(".")
        # go through the array and get the passengers
        for entry in array:
            if "passenger" in entry:
                makePassengerFromString(entry)
    r.close()


# extract numbers from strings
def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))


def makePassengerFromString(string):
    # create a passenger object
    temp = Passenger()

    # get the data from the string
    removePassengerString = string.replace("passenger", '')
    removeParensString1 = removePassengerString.replace("(", '')
    stringWithCommas = removeParensString1.replace(")", '')
    array = stringWithCommas.split(",")

    # construct passenger data
    temp.name = array[0]
    temp.startStation = int(array[1])
    temp.exitStation = int(array[2])

    # add them to the list
    passengers.append(temp)


def tick():
    subway.currentStation += 1

    # add the people that get on at station one
    for i in range(0, len(passengers)):
        if passengers[i].startStation is subway.currentStation:
            subway.passengers.append(passengers[i])


def createPrice(x):
    price = 0
    if x is 0:
        return price
    elif x is 1:
        return 1.0
    elif x is 2:
        return 1.9
    elif x is 3:
        return 2.7
    elif x is 4:
        return 3.4
    elif x is 5:
        return 4.0
    elif x is 6:
        return 4.5
    elif x is 7:
        return 4.9
    elif x is 8:
        return 5.2
    elif x is 9:
        return 5.4
    elif x is 10:
        return 5.5
    else:
        return 5.5


def calculateTotalCost():
    totalCost = 0
    for i in range(0, len(subway.passengers)):
        stationsTraveled = subway.passengers[i].exitStation - subway.passengers[i].startStation
        price = createPrice(stationsTraveled)
        totalCost += price
        round(totalCost, 1)

    return float(format(totalCost, '.1f'))


def main(fileName):
    openFile(fileName)

    startList = []
    exitList = []
    priceList = []

    for i in range(0, len(passengers)):
        exitList.append(passengers[i].exitStation)

    for i in range(0, len(passengers)):
        startList.append(passengers[i].startStation)

    subway.startStation = min(startList)
    subway.currentStation = 0
    subway.endStation = max(exitList)
    subway.passengers = []

    # put all the passengers on the train and the train at the end
    for i in range(subway.startStation, subway.endStation+1):
        tick()

    totalCost = calculateTotalCost()

    perms = list(itertools.permutations(startList))

    for i in range(0, len(perms)):
        for j in range(0, len(subway.passengers)):
            subway.passengers[j].startStation = perms[i][j]
        priceList.append(calculateTotalCost())

    for i in range(0, len(priceList)):
        priceList[i] = totalCost - priceList[i]

    print("loss(", float(format((max(priceList)), '.1f')), ").")

main(sys.argv[1])