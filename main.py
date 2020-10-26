#author: Md lutfar Rahman
#mrahman9@memphis.edu

from tkinter import *
from mygui import *
import nltk
import csv 
import random

testdata = './data/testdata.manual.2009.06.14.csv'
traindata = './data/training.1600000.processed.noemoticon.csv'


class MainClass(object):
    """docstring for MainClass"""
    def __init__(self, traindataFile):
        self.traindataFile = traindataFile
        self.classifier = None

    def readRawData(self,file):
        allrows=[]
        with open(file, 'r', encoding = "ISO-8859-1") as myfile:
            reader = csv.reader(myfile)
            for row in reader:
                if row[0]=='4':
                    emotion = 'Positive'
                elif row[0]=='0':
                    emotion = 'Negative'
                else:
                    emotion = 'Neutral'
                allrows.append((row[5],emotion))
                pass
        return allrows

    def prepare_train_set(self, file):
        pos_tweets = []
        neg_tweets = []
        neu_tweets = []
        limit = 500
        with open(file, 'r', encoding = "ISO-8859-1") as myfile:
            reader = csv.reader(myfile)
            #print(type(reader))
            for row in reader:
                if row[0]=='4':
                    emotion = 'Positive'
                elif row[0]=='0':
                    emotion = 'Negative'
                else:
                    emotion = 'Neutral'

                if emotion == 'Positive' and len(pos_tweets)<limit:
                    pos_tweets.append((row[5],emotion))
                elif emotion == 'Negative' and len(neg_tweets)<limit:
                    neg_tweets.append((row[5],emotion))
                elif  emotion == 'Neutral' and len(neu_tweets)<limit:
                    neu_tweets.append((row[5],emotion))

               
                if(len(pos_tweets) >= limit and len(neg_tweets) >= limit) and len(neu_tweets) >= limit:
                    return pos_tweets + neg_tweets + neu_tweets
        
        return pos_tweets + neg_tweets + neu_tweets

    def get_words_in_tweets(self,tweets):
        all_words = []
        for (words, sentiment) in tweets:
          all_words.extend(words)
        return all_words

    def get_word_features(self,wordlist):
        wordlist = nltk.FreqDist(wordlist)
        #print(wordlist)
        word_features = wordlist.keys()
        return word_features

    def extract_features(self,document):
        document_words = set(document)
        #print(document_words)
        features = {}
        for word in self.word_features:
            features['contains(%s)' % word] = (word in document_words)

        #print(features)
        return features

    def formate_data(self,rawData):
        tweets = []
        for (words, sentiment) in rawData:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
            tweets.append((words_filtered, sentiment))
        
        return tweets

    def prepareTrainData(self):
        raw_tweets = self.prepare_train_set(self.traindataFile)
        #print(len(raw_tweets))
        tweets = self.formate_data(raw_tweets)
        #print(tweets)
        self.word_features = self.get_word_features(self.get_words_in_tweets(tweets))
        #print(self.word_features[0])

        self.training_set = nltk.classify.apply_features(self.extract_features, tweets) 
   

    def train(self):
        self.classifier = nltk.NaiveBayesClassifier.train(self.training_set)
        return self.classifier


    def test(self, classifier, test_tweets):
        tp=0
        fp=0
        fn=0
        for tweet in test_tweets:
            result = classifier.classify(self.extract_features(tweet[0].split()))
            if result == tweet[1] and result == 'Positive':
                tp+=1
            elif result != tweet[1] and result == 'Positive':
                fp+=1
            elif result != tweet[1] and result == 'Negative':
                fn+=1


        return self.getPrecision(tp,fp,fn), self.getRecall(tp,fp,fn)

    def getPrecision(self,tp,fp,fn):
        return tp/(tp+fp)

    def getRecall(self,tp,fp,fn):
        return tp/(tp+fn)

    def classify(self, tweet):
        if not self.classifier:
            self.train()
        return self.classifier.classify(self.extract_features(tweet.split()))


    def TrainAll(self):
        trainers = [nltk.NaiveBayesClassifier, nltk.MaxentClassifier]

        classifiers = []
        for trainer in trainers:
            classifier = trainer.train(self.training_set)
            classifiers.append(classifier)

        return classifiers

    def runSingleExperiment(self, classifiers, tweet):
        results = []
        for classifier in classifiers:
            result = classifier.classify(self.extract_features(tweet.split()))
            results.append(result)

        return results


    def runExperiment(self):
        #classifiers = self.TrainAll()
        # #print(classifiers)
        # tweet = "I love you"

        # results = self.runSingleExperiment(classifiers, tweet)

        # print(self.extract_features(tweet.split()))
        test_tweets = self.readRawData(testdata)
        #classifier = self.train()
        p,r = self.test(self.classifier, test_tweets)
        
        return p,r




if __name__ == "__main__":

    model = MainClass(traindata)
    model.prepareTrainData()
    #model.runExperiment()

    root = Tk()
    my_gui = MyGUI(root, model)
    root.mainloop()

    print("end")
