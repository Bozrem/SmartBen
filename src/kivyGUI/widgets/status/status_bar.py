from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory

class StatusBar(BoxLayout):
    def __init__(self, **kwargs):
        super(StatusBar, self).__init__(**kwargs)

    def update_widgets(self, widget_info):
        self.ids.left_box.clear_widgets()
        self.ids.center_box.clear_widgets()
        self.ids.right_box.clear_widgets()

        for info in widget_info:
            widget = self.create_widget(info['name'])
            position = info['position']
            
            if position == 'left':
                self.ids.left_box.add_widget(widget)
            elif position == 'center':
                self.ids.center_box.add_widget(widget)
            elif position == 'right':
                self.ids.right_box.add_widget(widget)

    def create_widget(self, widget_name):
        return Factory.get(widget_name)()
