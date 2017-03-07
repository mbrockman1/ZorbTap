from random import randint
import os
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound

import sys

from kivyparticle import ParticleSystem


class StartButton(Widget):
    '''
    Creates start button that, when pressed, will carry over to game.
    '''

    def __init__(self, score, game, sound):
        super(StartButton, self).__init__()
        self.start_label = None
        self.high_score_controller = score
        self.high_score_label = None
        self.sound = sound
        self.game_widget = game
        self.start_button()

    def start_button(self):
        title_location = (Window.size[0] * .5, Window.size[1] * 0.65)
        self.title = Label(text="ZorbTap",
                           font_name='sanregular.ttf',
                           halign='center', font_size='40sp', size=('1', '1'),
                           pos=title_location)
        self.start_label = Button(font_size='20sp', halign='center',
                                  font_name='sanregular.ttf',
                                  size=Window.size, valign='middle',
                                  text=("Tap the Zorb Ship to destroy\n"
                                        "it before it gets away!\n"
                                        "Tap to Start"),
                                  background_color=[0, 0, 0, 0])
        music_button_location = (Window.size[0] * .70, Window.size[1] * 0.87)
        self.music_button = Button(font_size='20sp', halign='right', text=("Music"),
                                   valign='middle', size=('100sp', '100sp'),
                                   font_name='sanregular.ttf', background_color=[0, 0, 0, 0],
                                   pos=music_button_location)
        high_score_location = (Window.size[0] * .09, Window.size[1] * 0.87)
        self.high_score_label = Label(text="High Score: %s" % str(
            self.high_score_controller.get_high_score_for_start()),
                                      font_name='sanregular.ttf', valign='middle',
                                      halign='left', font_size='20sp', size=('100sp', '100sp'),
                                      pos=high_score_location)
        self.music_button.bind(on_release=self.music_controller)
        self.start_label.bind(on_release=self.start)
        self.add_widget(self.title)
        self.add_widget(self.start_label)
        self.add_widget(self.high_score_label)
        self.add_widget(self.music_button)

    def music_controller(self, touch):
        if self.sound.is_playing:
            self.sound.stop()
            self.sound.is_playing = False
        else:
            self.sound.play()
            self.sound.is_playing = True

    def start(self, touch):
        self.clear_widgets()
        self.game_widget.start()
        self.add_widget(self.game_widget)
        self.remove_widget(self.music_button)
        self.start_label.unbind(on_release=self.start)
        del self.music_button, self.high_score_label, self.start_label, self.title
        return super(StartButton, self).on_touch_down(touch)

class RestartButton(Widget):
    '''
    Creates restart button that, when pressed, will carry over to game.
    '''
    score = None

    def __init__(self, score, game, sound):
        super(RestartButton, self).__init__()
        self.loss_label = None
        self.sound = sound
        self.high_score_controller = score
        self.game_widget = game
        self.clear_widgets()
        self.loss_button()

    def loss_button(self):
        # Tells your score
        title_location = (Window.size[0] * .5, Window.size[1] * 0.65)
        self.title = Label(text="Zorb Escaped!",
                    font_name='sanregular.ttf',
                    halign='center', font_size='40sp', size=('1', '1'),
                    pos=title_location)
        self.loss_label =\
            Button(font_size='20sp', halign='center',
                   size=Window.size, valign='middle',
                   font_name='sanregular.ttf',
                   text=("You missed the last Zorb!\n" +
                         "It is free to do malicious Zorb things.\n" +
                         "Your score was %s\nTap to try again" %
                         str(self.high_score_controller.recent_score)),
                   background_color=[0, 0, 0, 0])
        music_button_location = (Window.size[0] * .70, Window.size[1] * 0.87)
        self.music_button = Button(font_size='20sp', halign='right', text=("Music"),
                                   valign='middle', size=('100sp', '100sp'),
                                   font_name='sanregular.ttf', background_color=[0, 0, 0, 0],
                                   pos=music_button_location)
        self.music_button.bind(on_release=self.music_controller)
        high_score_location = (Window.size[0] * .09, Window.size[1] * 0.87)
        self.high_score_label = Label(text="High Score: %s" % str(
            self.high_score_controller.get_high_score_for_start()),
                                      font_name='sanregular.ttf', valign='middle',
                                      halign='left', font_size='20sp', size=('100sp', '100sp'),
                                      pos=high_score_location)
        self.loss_label.bind(on_press=self.restart)
        self.add_widget(self.title)
        self.add_widget(self.loss_label)
        self.add_widget(self.high_score_label)
        self.add_widget(self.music_button)

    def music_controller(self, touch):
        if self.sound.is_playing:
            self.sound.stop()
            self.sound.is_playing = False
        else:
            self.sound.play()
            self.sound.is_playing = True

    def restart(self, *args):
        self.canvas.clear()
        self.loss_label.unbind(on_press=self.restart)
        self.game_widget.start()
        self.remove_widget(self.music_button)
        self.add_widget(self.game_widget)
        del self.music_button, self.high_score_label, self.loss_label, self.title
