import kivy

from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string('''
<LoginScreen>:
    id: login_screen

    MDCard:
        size_hint_y: None
        size_hint_x: 0.7
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 25
        spacing: 50
        orientation: 'vertical'
        height: self.minimum_height


        MDLabel:
            id: welcome_label
            text: "Hello"
            font_size: 100
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15

        MDTextField:
            mode: "round"
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: 0.7
            height: self.minimum_height

            font_size: 50
            pos_hint: {"center_x": 0.5}

        MDTextField:
            mode: "round"
            id: password
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: 0.7
            height: self.minimum_height

            font_size: 50
            pos_hint: {"center_x": 0.5}
            password: True

        MDRoundFlatButton:
            text: "LOG IN"
            font_size: 50
            pos_hint: {"center_x": 0.5}
            on_press: app.logger()

        MDRoundFlatButton:
            text: "CLEAR"
            font_size: 50
            pos_hint: {"center_x": 0.5} 
            on_press: app.clear()           

        Widget:
            size_hint_y: None
            height: 10''')


class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        logged = Label(text='logged')
        button_settings = Button(text='Go to settings', on_press=self.go_to_settings)

        layout.add_widget(logged)
        layout.add_widget(button_settings)
        self.add_widget(layout)

    def go_to_settings(self, *args):
        # self.manager.current='settings'
        print('пока такого экрана нет')


class SamuraiPath(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'BlueGray'
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

    def logger(self):
        # self.root.ids.screenmanager.ids.welcome_label.text = f'Sup {self.root.ids.user.text}!'
        a = self.root.ids.screenmanager.ids.welcome_label.text
        print(a)

    def clear(self):
        self.root.ids.welcome_label.text = "Work"
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""


if __name__ == '__main__':
    SamuraiPath().run()