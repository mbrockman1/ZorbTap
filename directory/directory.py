from kivy.app import App

class Directory(App):
    def __init__(self):
        super(type(self), self).__init__()
        SAVE_DIRECTORY = self.get_running_app().user_data_dir
