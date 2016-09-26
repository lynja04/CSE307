class Passenger:
    pass

passengers = list()


# open and parse file
def openFile():
    # open input file and parse the data
    r = open("tickettest.txt", "r")
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
    temp.entryStation = int(array[1])
    temp.exitStation = int(array[2])

    # add them to the list
    passengers.append(temp)

def main():
    openFile()

    for i in range(0, len(passengers)):
        print(passengers[i].name)

main()
