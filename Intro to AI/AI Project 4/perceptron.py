# perceptron.py
# -------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation
import util
PRINT = True

class PerceptronClassifier:
    """
    Perceptron classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        for label in legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels);
        self.weights = weights;

    def train(self, trainingData, trainingLabels, validationData, validationLabels ):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).
        """

        self.features = list(trainingData[0].keys()) # could be useful later
        # print("Features:\n", self.features)
        # print("Legal labels:\n", self.legalLabels)
        # print("Weights:\n", self.weights)
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.
        # print("# of Training Data sets: ", str(len(trainingData)))
        # print("# of Training Labels: ", str(len(trainingLabels)))
        # print("Training Labels: ", trainingLabels)
        # print("Validation Labels: ", validationLabels)
        # print("Validation Data:\n", len(validationData))

        # util.raiseNotDefined()
        for iteration in range(self.max_iterations):
            # set up a score counter to track the score for each label
            score = util.Counter()
            for label in self.legalLabels:
                score[label] = 0
            print(("Starting iteration ", iteration, "..."))
            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                # Question 3
                # Will utilize add, sub, and multiply functionality of counter.
                # Weights are already set up. Use legal labels as a key
                # print("Training Data in instance ", i, "\n", trainingData[i])
                # Each label needs its own Counter full of weights.
                # print("Weight values for example 0:\n", self.weights[0])

                # Current training label can be found with trainingLabel[i]
                trueLabel = trainingLabels[i]
                # Current training data is in trainingData[i]
                curData = trainingData[i]

                """
                Scoring
                Score of a label in a feature set = 
                Sum of all feature values * equivalent weight value for the equivalent label.
                Done by classify for the entire training data set
                """
                # iterate through each datum's feature set and run the score calculation
                # Classify iterates through every datum in the training data and returns the guessed label at an
                # equivalent index.
                # References the important part of classify to only calculate the weights for the current training set only
                guessVectors = util.Counter()
                for label in self.legalLabels:
                    guessVectors[label] = self.weights[label] * trainingData[i]
                guess = guessVectors.argMax()
                highestScoredGuessLabel = guess
                # print("Guessed label for current training set: ", highestScoredGuessLabel, " True label for current training set: ", trueLabel)
                if highestScoredGuessLabel == trueLabel:
                    # print("Labels Match!")
                    continue
                else:
                    # print("Wrong guess")
                    # Add the feature to the true label's weight, subtract from the guessed one
                    self.weights[trueLabel] = self.weights[trueLabel] + curData
                    self.weights[highestScoredGuessLabel] = self.weights[highestScoredGuessLabel] - curData
                    continue

        # util.raiseNotDefined()
        return

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        featuresWeights = []

        "*** YOUR CODE HERE ***"
        # Question 4
        orderedFeatureWeights = self.weights[label].sortedKeys()
        for i in range(99):
            featuresWeights.append(orderedFeatureWeights[i])

        return featuresWeights
