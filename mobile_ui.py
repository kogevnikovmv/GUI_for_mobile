import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput




class MainApp(App):
	def build(self):
		main_page=BoxLayout(
			orientation="vertical",
			padding=50,
			spacing=50
		)
		label = Label(text='Hello, User!', size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
		main_page.add_widget(label)

		login=TextInput(
			size_hint=(.5, .1),
			pos_hint={'center_x': .5, 'center_y': .5}
		)
		main_page.add_widget(login)

		password=TextInput(
			size_hint=(.5, .1),
			pos_hint={'center_x': .5, 'center_y': .5}
		)
		main_page.add_widget(password)

		login_button=Button(
			text='LogIn',
			size_hint=(.3, .2),
			pos_hint={'center_x': .5, 'center_y': .5})
		login_button.bind(on_press=self.login)
		main_page.add_widget(login_button)
		return main_page

	def login(self, instance):
		home_page=HomePage()
		return home_page

class HomePage(App):
	def build(self):
		home_page = BoxLayout(
			orientation="vertical",
			padding=50,
			spacing=50
		)
		label = Label(text='It\'s work', size_hint=(.5, .5), pos_hint={'center_x': .5, 'center_y': .5})
		home_page.add_widget(label)

		return home_page



if __name__ == '__main__':
	app = MainApp()
	app.run()