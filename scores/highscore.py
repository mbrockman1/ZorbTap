from kivy.uix.widget import Widget
import cPickle as pickle
import collections
from time import time
import os
import sys
from directory.directory import Directory


class HighScore(Widget):

    def __init__(self, score):
        super(HighScore, self).__init__()
        self.save_dir = Directory().user_data_dir
        self.HIGH_SCORE = 0
        self.recent_score = 0
        self.file_name = "high_score.pkl"
        self.file_location =\
            self.save_dir + "/" + self.file_name
        self.we_can_pickle_that()

    def update_high_score(self, passed_score):
        if passed_score > self.HIGH_SCORE:
            self.HIGH_SCORE = passed_score
            self.we_can_pickle_that()
        return int(self.HIGH_SCORE)

    def we_can_pickle_that(self):
        if not (os.path.isfile(self.save_dir + "/" + self.file_name)):
            with open(self.file_location, "wb") as fileObject:
                pickle.dump([self.HIGH_SCORE], fileObject)
                fileObject.close()

        else:
            with open(self.file_location, "rb") as fileObject:
                file_to_update = pickle.load(fileObject)
                fileObject.close()
            os.remove(self.file_location)
            file_to_update.append(self.HIGH_SCORE)
            self.HIGH_SCORE = max(file_to_update)
            with open(self.file_location, "wb") as fileObject:
                pickle.dump(file_to_update, fileObject)
                fileObject.close()

    def get_high_score_for_start(self):
        with open(self.file_location, "rb") as fileObject:
            getting_high_score = pickle.load(fileObject)
            fileObject.close()
        return max(getting_high_score)
