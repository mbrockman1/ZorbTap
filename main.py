import os
from sys import platform

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.audio import SoundLoader


from scores.highscore import HighScore
from buttons.buttons import StartButton
from game.game import SquareTapWidget
from kivyparticle import ParticleSystem


class ParentWidget(Widget):
    '''
    Creates parent Widget for overarching controller
    '''
    def __init__(self):
        super(ParentWidget, self).__init__()
        self.high_score = HighScore(0)
        self.start = None
        self.sound = None
        self.game_controller()

    def game_controller(self):
        self.sound = SoundLoader.load(os.getcwd() + '/media/space.wav')
        self.sound.loop = True
        self.sound.is_playing = True
        self.sound.play()
        self.star = ParticleSystem('media/star.pex')
        self.star.emitter_x = Window.size[0] / 2
        self.star.emitter_y = Window.size[1] / 2
        self.add_widget(self.star)
        self.star.start()
        self.start = StartButton(
            self.high_score, SquareTapWidget(self.high_score, self.sound), self.sound)
        self.start.background_color = (255, 255, 0)
        self.add_widget(self.start)


class SquareTapApp(App):
    '''
    Starts app
    '''

    def __init__(self):
        super(SquareTapApp, self).__init__()
        self.save_directory = None

    def build(self):
        parent = ParentWidget()
        return parent


if __name__ == '__main__':
    app_instance = SquareTapApp()
    if platform == 'android':
        import android.activity
        android.activity.bind(on_new_intent=app_instance.android_message)
    elif platform == 'ios':
        Window.bind(on_dropfile=app_instance.ios_message)
    app_instance.run()
