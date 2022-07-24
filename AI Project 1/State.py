"""
States.py module contains the States class definition and related functions that support it. See the class definition
below for details.
Author: Nicholas Duncan
Version: 2/4/2022
Email: N01451197@unf.edu
"""

"""
The State class contains the definition for a State object. This includes information such as state name, capitol, and
region as well as various covid related information. There are some variables within the object that calculate
automatically such as case rate, death rate, and case fatality rate.
an str and gt are included that are reponsible for printing out a state report and calculating if two states are equal
based on a inputted name.
"""


class State:
    # Global count of states
    stateCount = 0

    # object initialization
    def __init__(self, statename, capitol, region, ushouseseats, population,
                 covidcases, coviddeaths, fullvacrates, medhouseincome, vcrimerate):
        self.statename = statename
        self.capitol = capitol
        self.region = region
        self.ushouseseats = int(ushouseseats)
        self.population = int(population)
        self.covidcases = int(covidcases)
        self.coviddeaths = int(coviddeaths)
        self.fullvacrates = float(fullvacrates) / 100
        self.medhouseincome = int(medhouseincome)
        self.vcrimerate = float(vcrimerate)
        # Calculated data
        self.caserate = float(covidcases) / float(population) * 100000
        self.deathrate = float(coviddeaths) / float(population) * 100000
        self.casefatalityrate = float(coviddeaths) / float(covidcases)
        # Incremenet global state count
        State.stateCount += 1

    # Get state name
    def getstatename(self):
        return self.statename

    # Set state name
    def setstatename(self, name):
        self.statename = name

    # Get state capitol
    def getcapitol(self):
        return self.capitol

    # Set state capitol
    def setcapitol(self, name):
        self.capitol = name

    # Get state region
    def getstateregion(self):
        return self.region

    # Set state region
    def setstateregion(self, name):
        self.region = name

    # Get state US house seats
    def getstateseats(self):
        return self.ushouseseats

    # Set state US house seats
    def setstateseats(self, seats):
        self.statename = seats

    # Get state population
    def getstatepop(self):
        return self.population

    # Set state population
    def setstatepop(self, pop):
        self.population = pop

    # Get state covid cases
    def getstatecases(self):
        return self.covidcases

    # Set state covid cases
    def setstatecases(self, cases):
        self.covidcases = cases

    # Get state covid deaths
    def getstatedeaths(self):
        return self.coviddeaths

    # Set state covid deaths
    def setstatedeaths(self, deaths):
        self.coviddeaths = deaths

    # Get state full vaccine rates
    def getstatevacrates(self):
        return self.fullvacrates

    # Set state full vaccine rates
    def setstatevacrates(self, rates):
        self.fullvacrates = rates

    # Get state median household income
    def getstatemedhouseincome(self):
        return self.medhouseincome

    # Set state median household income
    def setstatemedhouseincome(self, income):
        self.medhouseincome = income

    # Get state violent crime rate
    def getstatevcrimerate(self):
        return self.vcrimerate

    # Set state violent crime rate
    def setstatevcrimerate(self, rate):
        self.vcrimerate = rate

    # Rates for case and death rates are automatically calculated based on their respective prerequisites
    # Get state case rate
    def getstatecaserate(self):
        return self.caserate

    # Get state death rate
    def getstatedeathrate(self):
        return self.vcrimerate

    # Get state case fatality rate
    def getstatecasefatalityrate(self):
        return self.casefatalityrate

    # method for printing an object like a string
    def __str__(self):
        """
        Prints our an organized state report based on given specifications such as decimal precision.
        :return: Nothing
        """
        # Name, Median Household income, Violent Crime rate,
        # Case fatality rate, Case Rate, Death Rate, and Full Vaccination Rate
        print("Name:\t\t" + self.statename)
        print("MHI:\t\t" + str(self.medhouseincome))
        print("VCR:\t\t" + str(round(self.vcrimerate, 1)))
        print("CFR:\t\t" + str(round(self.coviddeaths, 6)))
        print("Case Rate:\t\t" + str(round(self.caserate, 2)))
        print("Death Rate:\t\t" + str(round(self.deathrate, 2)))
        print("FV Rate:\t\t" + str(round(self.fullvacrates, 3)))

    # method for comparing two objects via name
    # If the current object is greater than the other, it will return True
    def __gt__(self, otherstate):
        """
        Does a simple True or False comparison of the current statename and a given one
        :param otherstate: Another string, preferably a state name
        :return: A boolean value
        """
        return self.statename > otherstate
