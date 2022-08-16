# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
        self.prior = util.Counter()
        self.conditionalsOn = []
        self.conditionalsOff = []

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in list(datum.keys()) ]));

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    # calculates the prior distribution from a set of training data
    # Returns a counter object (label):Value
    def calcPrior(self, trainingLabels):
        # P(Y) for each label is equal to the amount of training instances that are expected to use the label / total instances
        # calculate total training instances
        total = len(trainingLabels)
        # Initialize counter
        priorDist = util.Counter()
        # Initialize the legal labels onto the prior distribution, allows it to start off sorted by label
        for label in self.legalLabels:
            priorDist[label] = 0
        # Run through list of expected labels and add 1 to respective counter.
        for label in trainingLabels:
            priorDist[label] += 1
        # Use divide all counter function to divide all calculated label values by the total number of instances
        priorDist.divideAll(total)
        # apply log to each of the label's prior distribution value
        for label in self.legalLabels:
            priorDist[label] = math.log(priorDist[label])
        # Assign the newly calculated prior distribution set to the constructor variable.
        self.prior = priorDist
        return priorDist

    def calcCond(self, data, labels, k):
        # Conditional probability for a given label is based on how many times a feature is on or off across
        # all data sets

        # Calculate the # of total training instances per label, each respective total will divide the top part
        # of the equation
        labelTotals = util.Counter()
        for label in labels:
            labelTotals[label] += 1
        # Add the smoothing value to each
        for label in self.legalLabels:
            labelTotals[label] += k

        # store values in a 2d array
        # conditionals[label][off or on (0 or 1)] = counter (feature): times a specific value was picked
        # Calculate the times a given value was on or off through each instance for it's respective expected label
        condOn = []
        condOff = []
        for label in self.legalLabels:
            condOn.append(util.Counter())
            condOff.append(util.Counter())
            # Fill each counter with features to hopefully help keep them sorted in order
            for feature in self.features:
                condOn[label][feature] = k
                condOff[label][feature] = k
        # print("on condition for label 0:\n", condOn[0])

        # run through training data and labels and calculate each of the conditionals
        for i in range(len(data)):
            # Record the current datum and its respective expected label
            curLabel = labels[i]
            datum = data[i]
            # Iterate through each feature and based on the value add to the respected conditional list
            for feature in self.features:
                curValue = datum[feature]
                if curValue == 1:
                    condOn[curLabel][feature] += 1

                elif curValue == 0:
                    condOff[curLabel][feature] += 1

                else:
                    print("WARNING: Unexpected value")
                    exit()
            """# Add k to each feature calculation within the current label
            for feature in self.features:
                # Add in smoothing value
                condOn[curLabel][feature] += k
                # Add in smoothing value
                condOff[curLabel][feature] += k"""
        # Divide each feature key value by the times it's smoothed equivalent label appears in the training set
        for label in self.legalLabels:
            condOn[label].divideAll(labelTotals[label])
            condOff[label].divideAll(labelTotals[label])
            # print(condOn[label])
        self.conditionalsOn = condOn.copy()
        self.conditionalsOff = condOff.copy()


    # Compare the original
    def compare(self, targetlist,originlist):
        matches = 0
        mismatches = 0
        for i in range(len(originlist)):
            if originlist[i] == targetlist[i]:
                matches += 1
            else:
                mismatches += 1
        # print("Matches: ", matches, " Mismatches: ", mismatches)
        # Calculate percentage of matches to the second decimal place
        return matches / len(originlist)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """

        "*** YOUR CODE HERE ***"
        # Question 1
        # All possible features and legal labels
        # Features are coordinate tuples that represent pixel locations
        # labels are the possible number that could be represented

        # Calculate Prior distribution P(Y) with a function call
        # LOG CALCULATIONS ARE ALREADY PERFORMED ON THE DATA
        self.calcPrior(trainingLabels)
        print("Prior distribution:\n", self.prior)

        # test smoothing values
        smoothedResults = util.Counter()
        for k in kgrid:
            self.calcCond(trainingData, trainingLabels, k)
            # print(self.smoothedCond[0])
            returned = self.classify(validationData)
            # print("Returned from classify:\n", returned)
            smoothedResults[k] = self.compare(returned, validationLabels)

        print("Smoothing results for all k values from validation data:\n", smoothedResults)

        smoothedlist = smoothedResults.sortedKeys()
        print("Sorted key values:\n", smoothedlist)

        # Select the k with the highest accuracy and run the conditional and classifying again
        bestacc = 0
        bestk = 0
        for i in range(len(smoothedlist)):
            if smoothedResults[smoothedlist[i]] > bestacc:
                bestacc = smoothedResults[smoothedlist[i]]
                bestk = smoothedlist[i]
            elif smoothedResults[smoothedlist[i]] == bestacc and bestk > smoothedlist[i]:
                bestk = smoothedlist[i]
        print("The best k value is: ", bestk)


        self.calcCond(trainingData, trainingLabels, bestk)
        self.classify(trainingData)

        # util.raiseNotDefined()
        return

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """

        "*** YOUR CODE HERE ***"
        # Question 1
        # Called from classify
        logJoint = util.Counter()

        # Prior is stored as a counter with {(label): log of prior dist value}
        # Conditional is stored as {(label): conditional probability for each label to be on}
        # Perform a log joint distribution calculation for each label in comparison with the current data set
        # store the result of the current label's calculation in a counter
        for label in self.legalLabels:
            # Prior distribution will be added at the end of the calculation
            curLogJointDist = 0
            # Prior distribution is a simple integer value
            curPrior = self.prior[label]
            # Counter holding the conditionals' probability for each feature to be on
            curConditionalOn = self.conditionalsOn[label]
            curConditionalOff = self.conditionalsOff[label]

            # Perform log joint calculation
            for feature in self.features:
                # Sum all the log conditionals values for all features
                # If the current feature is a 1, use the on conditional for a feature, if not, use the off
                value = 0
                if datum[feature] == 1:
                    value = curConditionalOn[feature]
                elif datum[feature] == 0:
                    value = curConditionalOff[feature]
                """# log cannot be applied to values of 0, so skip if they exist
                if value == 0:
                    continue"""
                curLogJointDist += math.log(value)

            # Add the prior distribution
            curLogJointDist += curPrior

            # Assign to the current label in the log joint counter
            logJoint[label] = curLogJointDist
        # print("Log joints for this datum: ", logJoint)
        return logJoint

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        featuresOdds = []
        # feature: calculated odd ratio
        compared = util.Counter()
        print(label1)
        tempfeatures = util.Counter()
        "*** YOUR CODE HERE ***"
        # Question 2
        for feature in self.features:
            compared[feature] = self.conditionalsOn[label1][feature] / self.conditionalsOn[label2][feature]
        ordered = compared.sortedKeys()
        for i in range(100):
            featuresOdds.append(ordered[i])
        # util.raiseNotDefined()
        return featuresOdds
