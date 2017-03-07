import os
from random import randint
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from buttons.buttons import RestartButton, StartButton

from kivyparticle import ParticleSystem


class SquareTapWidget(Widget):

    def __init__(self, high_score, sound):
        super(SquareTapWidget, self).__init__()
        self.sound = sound
        self.laser = SoundLoader.load(os.getcwd() + '/media/laser.wav')
        self.score = 0
        self.touch_of_x, self.touch_of_y = -1, -1
        self.spaceship = None
        self.color = None
        self.explosion = ParticleSystem('media/explosion.pex')
        self.high_score_controller = high_score
        self.bind(on_touch_down=self.on_touch_down)
        self.loss = None

    def on_touch_down(self, touch, *args):
        handled = super(type(self), self).on_touch_down(touch)
        self.touch_of_x, self.touch_of_y = touch.x, touch.y
        return handled

    def start(self):
        '''
        Start drawing a square; this is the square initialization
        '''
        self.high_score_controller.recent_score = 0
        self.canvas.clear()
        self.add_widget(self.explosion)
        self.draw_clock = Clock.schedule_once(self.draw)
        self.draw_clock()

    def draw(self, dt):
        '''
        Square is drawn
        '''
        self.bind(on_touch_down=self.on_touch_down)

        # Time progressively gets shorter
        self.time = ((20 / (1. + 2.714 ** (self.score / 10.))))

        # Set size and random position of Rectangle
        self.rect_size = (max(Window.width, Window.height) / 10,
                          max(Window.width, Window.height) / 10)
        self.window_pos = (randint(0, Window.width - self.rect_size[0]),
                           randint(0, Window.height - self.rect_size[1]))
        # Fixed for any screen
        self.secondary_time = max(
            float(self.time / self.rect_size[0]),
            float(self.time / self.rect_size[1]))
        # Call to draw
        self.spaceship = Image(source="media/spaceship.png",
                               pos=self.window_pos,
                               size=self.rect_size)
        # Function to progressively shrink rectangle
        self.add_widget(self.spaceship)
        self._rect_shrink_clock =\
            Clock.schedule_interval(self._rect_shrink, self.secondary_time)
        self._rect_shrink_clock()

    def _rect_shrink(self, dt):
        '''
        Clear the canvas so you can redraw a smaller square
        '''
        # Smaller size
        self.rect_size, self.window_pos = self._update_rect_size()
        self.spaceship.pos = self.window_pos
        self.spaceship.size = self.rect_size

        # If size is 0 then cancel the clock to draw another
        # Elif is touch within? if so clear canvas and redraw
        if ((self.window_pos[0] - 15 <= self.touch_of_x <=
             self.window_pos[0] + self.rect_size[0] + 15) and
                (self.window_pos[1] - 15 <= self.touch_of_y <=
                 self.window_pos[1] + self.rect_size[1] + 15)):
            self.laser.play()
            self.spaceship.size = (0, 0)
            self.remove_widget(self.spaceship)
            del self.spaceship
            self.explosion.emitter_x = self.touch_of_x
            self.explosion.emitter_y = self.touch_of_y
            self.explosion.start()
            Clock.schedule_once(self.clear_explosion, 0.2)

            # Set touch off screen so that square be marked as success
            self.touch_of_x, self.touch_of_y = -1, -1

            # score adition
            self.score = self.score + 1
            self._rect_shrink_clock.cancel()
            self.draw_clock()

        # if area = 0; LOSER
        elif (self.rect_size[0] is 0 or self.rect_size[1] is 0 or
              self.rect_size[0] * self.rect_size[1] == 0 or
              (self.spaceship.size[0] < 0.)):
            self.spaceship.size = (0, 0)
            self._rect_shrink_clock.cancel()
            self.draw_clock.cancel()
            self.clear_widgets()
            self.high_score_controller.update_high_score(self.score)
            self.unbind(on_touch_down=self.on_touch_down)
            self.loss = Clock.schedule_once(self.loss_button)
            self.loss()
            del self.explosion, self.spaceship, self.laser
            return self.score

    def clear_explosion(self, dt):
        self.explosion.stop()

    def loss_button(self, dt):
        # Tells your score
        self.high_score_controller.recent_score = self.score
        self.add_widget(
            RestartButton(self.high_score_controller,
                          SquareTapWidget(self.high_score_controller, self.sound), self.sound))

    def _update_rect_size(self):
        '''
        Rectangle size shrink functionality
        '''
        if self.score <= 25:
            width = self.rect_size[0] - 2
            height = self.rect_size[1] - 2
            pos_width = self.window_pos[0] + 1
            pos_height = self.window_pos[1] + 1
            return (width, height), (pos_width, pos_height)
        elif self.score > 25 and self.score <= 39:
            width = self.rect_size[0] - 4
            height = self.rect_size[1] - 4
            pos_width = self.window_pos[0] + 2
            pos_height = self.window_pos[1] + 2
            return (width, height), (pos_width, pos_height)
        else:
            width = self.rect_size[0] - 8
            height = self.rect_size[1] - 8
            pos_width = self.window_pos[0] + 4
            pos_height = self.window_pos[1] + 4
            return (width, height), (pos_width, pos_height)
