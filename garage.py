import re

class LicensePlate:
    def __init__(self, number):
        self.number = number

    def isInState(self):
        isOldFormat = re.search("^[A-Z]{3}-[0-9]{3,5}", self.number)
        isNewFormat = re.search("^[A-Z0-9]{3} [0-9]{4}", self.number)

        if isOldFormat or isNewFormat:
            return True
        else:
            return False

class Employee:
    def __init__(self, hexId, licensePlate, parkingSpaceType):
        self.hexId = hexId
        self.licensePlate = licensePlate
        self.parkingSpaceType = parkingSpaceType

        self.id = self.convertHexId()

    def convertHexId(self):
        id = ""

        for number in self.hexId[:-1]:
            id += str(int(number, 16)) + "-"
        id += str(int(self.hexId[-1], 16))
        
        return id

class ParkingSpace:
    occupant = None

    def __init__(self, type):
        self.type = type

    def occupy(self, employee):
        if not self.occupant:
            self.occupant = employee

        else:
            raise Exception("Parking space occupied by " + employee.id)

    def evacuate(self):
        if self.occupant:
            self.occupant = None

        else:
            raise Warning("Parking space already evacuated")

    def isOccupied(self):
        if self.occupant:
            return True

        else:
            return False

class ParkingGarage:
    numSpaces = {}
    spaces = []

    def __init__(self, numRegSpaces, numResSpaces, numHandiSpaces):
        self.numSpaces['regular'] = numRegSpaces
        self.numSpaces['reserved'] = numResSpaces
        self.numSpaces['handicap'] = numHandiSpaces

        self.initializeSpaces()

    def initializeSpaces(self):
        for spaceType, number in self.numSpaces.iteritems():
            for space in range(number):
                self.spaces.append(ParkingSpace(spaceType))

    def addCar(self, employee):
        for spaceNum, space in enumerate(self.spaces):
            if space.type is employee.parkingSpaceType and\
                not space.isOccupied():

                space.occupy(employee)
                return spaceNum

        return False

    def removeCar(self, employee):
        for spaceNum, space in enumerate(self.spaces):
            if space.isOccupied and space.occupant is employee:
                space.evacuate()

                return None

    def isFull(self):
        for space in self.spaces:
            if not space.isOccupied():
                return False
        
        return True

    def isEmpty(self):
        for space in self.spaces:
            if space.isOccupied():
                return False

        return True

    def numTotalSpaces(self):
        return len(self.spaces)

    def numTotalFullSpaces(self):
        fullCount = 0

        for space in self.spaces:
            if space.isOccupied():
                fullCount += 1

        return fullCount

    def numTotalFullPercent(self):
        return float(self.numTotalFullSpaces())/self.numTotalSpaces() * 100

    def numTotalEmptySpaces(self):
        return self.numTotalSpaces - self.numTotalFullSpaces()

    def numSpacesByType(self, spaceType):
        return self.numSpaces[spaceType]

    def numFullSpacesByType(self, spaceType):
        fullCount = 0

        for space in self.spaces:
            if space.type is spaceType and space.isOccupied():
                fullCount += 1

        return fullCount

    def numFullPercentByType(self, spaceType):
        return float(self.numFullSpacesByType(spaceType))/\
            self.numSpacesByType(spaceType) * 100

    def numEmptySpacesByType(self, spaceType):
        return self.numSpacesByType(spaceType) -\
        self.numFullSpacesByType(spaceType)

    def spaceOccupied(self, spaceId):
        return self.spaces[spaceId].isOccupied()

    def spaceOccupant(self, spaceId):
        return self.spaces[spaceId].occupant

    def displayStatus(self):
        print("Available Spaces:")
        for spaceType, number in self.numSpaces.iteritems():
            print("{0}: {1}/{2}".format(
                spaceType.capitalize(),
                str(self.numEmptySpacesByType(spaceType)),
                str(self.numSpacesByType(spaceType))))
