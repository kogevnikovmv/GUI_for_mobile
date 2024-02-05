from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super (MenuScreen,self).__init__(**kwargs)
        layout=BoxLayout(orientation='vertical')

        button_quit=Button(
            text='Quit'
        )
        button_settings=Button(
            text='Settings',
            on_press=self.go_to_settings)

        layout.add_widget(button_quit)
        layout.add_widget(button_settings)
        self.add_widget(layout)



    def go_to_settings(self, *args):
        self.manager.current='settings'

class Settings(Screen):
    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        layout = BoxLayout()

        settings = Label(
            text='It\'s your ettings'
        )
        button_back = Button(
            text='Go to menu',
            on_press=self.go_to_menu
        )

        layout.add_widget(settings)
        layout.add_widget(button_back)
        self.add_widget(layout)



    def go_to_menu(self, *args):
        self.manager.current='menu'

class TestApp(App):
    def build(self):
        sm=ScreenManager()
        screen1=MenuScreen(name='menu')
        screen2=Settings(name='settings')

        sm.add_widget(screen1)
        sm.add_widget(screen2)

        return sm

if __name__ == '__main__':
    TestApp().run()