from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton
from kivy.animation import Animation
from kivy.metrics import dp
from kivymd.uix.gridlayout import MDGridLayout

Builder.load_string('''
<LoginScreen>:
    id: login_screen

    MDGridLayout:
        cols: 1
        rows: 10
        id: card
        row_default_height: dp(50)
        size_hint_y: None
        size_hint_x: 0.7
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 10
        padding: 25
        spacing: 50
        orientation: 'tb-lr'
        height: self.minimum_height


        MDLabel:
            index: 0
            id: welcome_label
            text: "Hello"
            font_size: dp(44)
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15

        MDTextField:
            index: 1
            mode: "round"
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: 0.7
            height: self.minimum_height

            font_size: dp(19)
            pos_hint: {"center_x": 0.5}

        MDTextField:
            index: 2
            mode: "round"
            id: password
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: 0.7
            height: self.minimum_height

            font_size: dp(19)
            pos_hint: {"center_x": 0.5}
            password: True

        AnchorLayout:
            index: 3
            id: anchr_log
            MDRoundFlatButton:
                id: login_button
                text: "LOG IN"
                font_size: dp(19)
                pos_hint: {"center_x": 0.5}
                on_press: root.logger()

        AnchorLayout:
            index: 4
            MDRoundFlatButton:
                id: create_account
                text: "Create account"
                font_size: dp(19)
                pos_hint: {"center_x": 0.5} 
                on_press: root.remove()           

        Widget:
            size_hint_y: None
            height: 10

<HomeScreen>:
    id: homescreen
            ''')


class LoginScreen(Screen):

    def logger(self):
        self.ids.welcome_label.text = f'Hi {self.ids.user.text}!'
        self.manager.current = 'home'

    def remove(self):
        self.anim_remove(self.ids.login_button)
        self.anim_remove(self.ids.create_account)
        self.add()

    def add(self):
        self.ids.card.add_widget(MDTextField(
            mode='round',
            hint_text='email',
            icon_right='email',
            size_hint_x=.7,
            font_size=dp(19),
            pos_hint={'center_x': .5}), index=4)
        self.ids.card.add_widget(MDRoundFlatButton(
            text='Register',
            pos_hint={'center_x': .5},
            font_size=dp(19)), index=3)

    def new_account(self):
        self.ids.welcome_label.text = 'Register'
        # self.ids.card.remove_widget(self.ids.login_button)
        # self.anim_remove(self.ids.login_button)
        # self.ids.card.add_widget(MDTextField(

    #            mode='round',
    #            hint_text='email',
    #            icon_right='email',
    #            size_hint_x=.7,
    #            font_size=dp(19),
    #            pos_hint={'center_x':.5}), index=3)
    # self.ids.card.remove_widget(self.ids.create_account)
    # self.anim_remove(self.ids.create_account)
    # self.ids.card.add_widget(MDRoundFlatButton(
    #            text='Register',
    #            pos_hint={'center_x':.5},
    #            font_size=dp(19)), index=4)

    def anim_remove(self, item):
        anim = Animation(width=0, opacity=0, d=0.5)
        anim.bind(on_complete=lambda *args: self.ids.card.remove_widget(item))
        anim.start(item)

    def clear(self):
        self.ids.welcome_label.text = "Hello"
        self.ids.user.text = ""
        self.ids.password.text = ""


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


if __name__ == '__main__':
    SamuraiPath().run()
