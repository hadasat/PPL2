from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from backend import getRecommandations

popup = {}

class Pop(Widget):

    pop_text = ObjectProperty(None)

    def __init__(self, results):
        Widget.__init__(self)
        self.pop_text.text = results

    def closeBtn(self):
        popup["p"].dismiss()

class MainWindow(Screen):
    # all labels
    current_location = ObjectProperty(None)
    time = ObjectProperty(None)
    num_Recommendations = ObjectProperty(None)
    birth_year = ObjectProperty(None)
    male = ObjectProperty(None)
    female = ObjectProperty(None)

    gender = 2

    def searchBtn(self):
        error_list = self.is_valid_input()
        if error_list.__len__() == 0:
            self.recommendations([])
        else:
            self.recommendations("\n".join(error_list))
        self.reset()

    def reset(self):
        self.current_location.text = ""
        self.time.text = ""
        self.num_Recommendations.text = ""
        self.birth_year.text = ""
        self.male.active = False
        self.female.active = False
        self.gender = 2

    # check if the input is valid
    def is_valid_input(self):
        errors_list = []
        if self.current_location.text == "":
            errors_list.append("you need to insert current location")
        if not self.time.text.isdigit():
            errors_list.append("time must be numeric value")
        if not self.num_Recommendations.text.isdigit():
            errors_list.append("recommendations must be numeric value")
        if not self.birth_year.text.isdigit():
            errors_list.append("birth year must be numeric value")
        return errors_list

    # create a pop up with the error or the recommendations
    def recommendations(self, rec):
        # this case the input is invalid
        if type(rec) is str:
            content = Pop(rec)
            title = "Bad input"
        # the input is valid so we search for recommendations
        else:
            try:
                print(self.num_Recommendations.text)
                number_of_recommendations = int(self.num_Recommendations.text)
                trip_duration_min = int(self.time.text)
                start_station = self.current_location.text
                birth_year = int(self.birth_year.text)
                rec = getRecommandations(number_of_recommendations,trip_duration_min,start_station,birth_year,self.gender)
            except NameError:
                rec = [NameError]
            finally:
                if type(rec) == str:
                    rec = [rec, "please try again"]
                if not rec:
                    rec = ["with those input you", "better stay at home"]
            content = Pop("\n".join(rec))
            title = "Recommendations"

        popup['p'] = Popup(title=title, content=content, size_hint=(0.52, 0.8))
        popup['p'].open()

    def active_female(self):
        if self.female.active:
            self.gender = 0
        else:
            self.gender = 2

    def active_male(self):
        if self.male.active:
            self.gender = 1
        else:
            self.gender = 2


class MyApp(App):
    def build(self):
        self.title = 'Recommendations App'
        return MainWindow()


if __name__ == "__main__":
    MyApp().run()
