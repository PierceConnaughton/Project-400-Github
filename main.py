from typing import Text
import kivymd
import Load_Sentiment as sentiment
import Load_Generation as generate
import Twitter_API as api
from IPython import get_ipython
from kivymd.app import MDApp
from kivymd.uix.label import Label
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDRaisedButton
from kivy.uix.popup import Popup
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

#create a grid using the grid layout class from kivy        
class MyGrid(MDGridLayout):
    tweet = ObjectProperty(None)

    def resetScreen(self):
                self.tweet.text = ""
                self.ids.tweet_generated.text = "No Tweet Generated"
                self.ids.tweet_sentiment.text = "No Sentiment Detected"
    
    def PostTweet(self):
        tweet =  self.ids.tweet_generated.text
        sentiment =  self.ids.tweet_sentiment.text
        if tweet == '' or tweet == 'No Tweet Generated':
            popup = Popup(title='Tweet Could Not Be Posted',
            content=Label(text='Tweet cant be blank'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        elif sentiment == 'Negative sentiment':
            popup = Popup(title='Tweet Could Not Be Posted',
            content=Label(text='Tweet cant be negative'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        else:
            
            text = 'this a test tweet: ' + self.ids.tweet_generated.text
            #post status to twitter
            api.postStatus(text)
            popup = Popup(title='Tweet Posted',
            content=Label(text='The Tweet was posted successfully'),
            size_hint=(None, None), size=(400, 400))
            popup.open()

    #pressed method, when a button is pressed get the name value and print it too the console
    def pressed(self):
        text = self.tweet.text
        

        if text == '' :
            MyGrid.resetScreen(self)
        
        else:

            generated = generate.generateTweet(text)

            self.ids.tweet_generated.text = f'{generated} '


            #Check sentiment of generated tweet
            prediction = sentiment.predict(generated)
        
            self.ids.tweet_sentiment.text = f'{prediction} sentiment'


            #print name to screen
            print("Tweet:", text, " Sentiment: ", prediction, " Tweet Generated: ", generated)

            #reset name to blank
            self.tweet.text = ""



           

#class for Main app
class MainApp(MDApp):
    #build the app

    def build(self):
        self.theme_cls.primary_palette = "Green"
        screen = MDScreen()
        screen.add_widget(MyGrid())
        return screen

MainApp().run()