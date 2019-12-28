from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox


popup = {}

class Pop(Widget):

    pop_text = ObjectProperty(None)

    def __init__(self, results):
        Widget.__init__(self)
        self.pop_text.text = results+"\n"+results+"\n"+results+"\n"+results+"\n"+results+"\n"+results+"\n"+results+"\n"+results+"\n"+results+"\n"+results+"\n"

    def closeBtn(self):
        print("h")
        popup["p"].dismiss()


class MainWindow(Screen):
    current_location = ObjectProperty(None)
    time = ObjectProperty(None)
    num_Recommendations = ObjectProperty(None)
    birth_year = ObjectProperty(None)
    male = ObjectProperty(None)
    female = ObjectProperty(None)

    gender = {'M': False, 'F': True}


    def searchBtn(self):
        self.reset()
        list_rec = ""
        self.recommendations(list_rec)

    def reset(self):
        self.current_location.text = ""
        self.time.text = ""
        self.num_Recommendations.text = ""
        self.birth_year.text = ""
        self.male.active = False
        self.female.active = False


    def valid_loc(self,location):
        return True

    def is_valid_input(self, start_loc, time, rec_num, gender, b_year):
        valid_loc = self.valid_loc(self, start_loc)
        valid_date = time.isdigit()
        valid_rec = rec_num.isdigit()
        valid_gender = gender == 1 or gender == 0
        valid_yaer = b_year.isdigit()
        return valid_date and valid_gender and valid_loc and valid_rec and valid_yaer

    def recommendations(self, rec):
        if rec is None:
            content = Pop("pleas try again")
            title = "bad input"
        else:
            content = Pop("hello")
            title = "Recommendations"
        popup['p'] = Popup(title=title, content=content, size_hint=(0.52,0.8))
        popup['p'].open()
        print('hadas')

    def active_female(self):
        self.gender['F'] = True
        self.gender['M'] = False

    def active_male(self):
        self.gender['F'] = False
        self.gender['M'] = True

class MyApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    MyApp().run()
