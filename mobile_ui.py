from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.storage.jsonstore import JsonStore

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.image import Image

from kivy.clock import Clock
import requests

# описание логин скрина на kv language
Builder.load_string('''
<LoginScreen>:
    id: login_screen

    MDCard:
        id: card
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
            font_size: dp(44)
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15

        MDTextField:
            mode: "round"
            id: login
            hint_text: "username"
            icon_right: "account"
            size_hint_x: 0.7
            height: self.minimum_height

            font_size: dp(19)
            pos_hint: {"center_x": 0.5}

        MDTextField:
            mode: "round"
            id: password
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: 0.7
            height: self.minimum_height

            font_size: dp(19)
            pos_hint: {"center_x": 0.5}
            password: True

        Label:
            id: error_text
            text: ' '
            color: 'red'
            font_size: dp(10)
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]


        MDRoundFlatButton:
            id: login_button
            text: "Log In"
            font_size: dp(19)
            pos_hint: {"center_x": 0.5}
            on_press: root.login()

        MDRoundFlatButton:
            id: create_account
            text: "Create account"
            font_size: dp(19)
            pos_hint: {"center_x": 0.5} 
            on_press: root.anim_disappeare()           

        Widget:
            size_hint_y: None
            height: 10

<HomeScreen>:
    id: homescreen''')

# <LogoScreen>:
#    id: logoscreen
#    Image:
#        id: logo_img
#        source: 'static_files/main_logo.png'
#        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
#        size_hint_y: 0.7
#        size_hint_x: 0.7
#        fit_mode: 'contain'
#            ''')

storage = JsonStore('../data_app.json')



class LogoScreen(Screen):
    def __init__(self, **kwargs):
        super(LogoScreen, self).__init__(**kwargs)

        self.logo = Image(source='static_files/main_logo.png',
                          pos_hint={'center_x': .5, 'center_y': .5},
                          size_hint_y=.7,
                          size_hint_x=.7,
                          fit_mode='contain')
        self.add_widget(self.logo)

    def on_enter(self):
        try:
            token=storage.get('auth_token')['token']
        except(KeyError):
            screen='login'
        Clock.schedule_once(self.anim_disappeare(screen), 3)


    def authtorization(self):
        pass
        # не верно(

    def anim_disappeare(self, screen, *args):
        anim = Animation(opacity=0, d=0.5)
        anim.bind(on_complete=lambda *args: self.go_to_login(screen))
        anim.start(self.logo)

    def go_to_login(self, screen, *args):
        self.manager.current = screen


class LoginScreen(Screen):

    # идентификация пользователя
    def login(self):
        # получение пароля\логина по id
        login = self.ids.login.text
        password = self.ids.password.text
        # аутентификация
        if self.auth(login, password) == True:
            self.manager.current = 'home'
        else:
            self.ids.error_text.text = 'login/password incorrect'

    # пока имитация аутентификации
    def auth(self, login, password):
        response = requests.post('http://127.0.0.1:8000/login',
                                 json={"username": login, "password": password})
        if not response.json().get('token'):
            return False
        token=response.json().get('token')
        token = token.get('token')
        print(token)
        storage.put('auth_token', token=token)
        return True





    # анимация исчезновения окна логина
    # по ЗАВЕРШЕНИЮ анимации запускается ф-ция register
    def anim_disappeare(self):
        anim = Animation(opacity=0, d=0.5)
        anim.bind(on_complete=lambda *args: self.register())
        anim.start(self.ids.card)

    # анимация появления окна регистрации
    def anim_appeare(self):
        anim = Animation(opacity=1, d=0.5)
        anim.start(self.ids.card)

    # изменение логин формы в регистрационную форму
    # все изменения происходят пока форма невидима
    def register(self):
        self.ids.error_text.text = ' '
        self.ids.login.text = ''
        self.ids.password.text = ''
        self.ids.welcome_label.text = 'Register'
        self.ids.card.remove_widget(self.ids.login_button)
        self.ids.card.add_widget(MDTextField(
            mode='round',
            hint_text='email',
            icon_right='email',
            size_hint_x=.7,
            font_size=dp(19),
            pos_hint={'center_x': .5}), index=3)
        self.ids.card.remove_widget(self.ids.create_account)
        self.ids.card.add_widget(MDRoundFlatButton(
            text='Register',
            pos_hint={'center_x': .5},
            font_size=dp(19)), index=1)
        self.anim_appeare()


# главное окно
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        logged = Label(text='logged')
        button_settings = Button(text='Go to settings', on_press=self.go_to_settings)

        layout.add_widget(logged)
        layout.add_widget(button_settings)
        self.add_widget(layout)

    # ф-ция смены экрана на settings
    def go_to_settings(self, *args):
        # self.manager.current='settings'
        print('пока такого экрана нет')


# главный класс, создаем скрин менеджера
class SamuraiPath(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'BlueGray'
        sm = ScreenManager()
        sm.add_widget(LogoScreen(name='logo'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        return sm


if __name__ == '__main__':
    SamuraiPath().run()
