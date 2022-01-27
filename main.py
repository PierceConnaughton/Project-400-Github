from logging import root
from tracemalloc import start
from turtle import left
from typing import Text
import kivymd
import Load_Sentiment as sentiment
import Load_Generation as generate
import Twitter_API as api
from IPython import get_ipython
from kivymd.app import MDApp
from kivymd.uix.label import Label
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDRaisedButton
from kivy.uix.popup import Popup
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty

# Create the screen manager
sm = ScreenManager()
tweetText = ''

# Declare both screens
class MenuScreen(Screen):

    tweet = ObjectProperty(None)
    generatedTweet = ObjectProperty(None)
    sentimentTweet = ObjectProperty(None)

    def resetScreen(self):
        tweet = self.ids.tweet.text

        if tweet == '':
            popup = Popup(title='Tweet Could Not Be Reset',
            content=Label(text='Tweet was has nothing to reset'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        else:
            self.ids.tweet.text = ''   

    def pressed(self):
        tweet = self.ids.tweet.text
        
        if tweet == '':
            popup = Popup(title='Tweet Could Not Be Submitted',
            content=Label(text='Tweet cant be blank'),
            size_hint=(None, None), size=(400, 400))
            popup.open()

        else:
            tweetText = tweet + ' '

            generatedTweet = generate.generateTweet(tweetText)
            sentimentTweet = sentiment.predict(generatedTweet)

            tweetScreen = self.manager.get_screen("tweet")
            tweetScreen.ids.tweet_generated.text = f'{generatedTweet} '
            tweetScreen.ids.tweet_sentiment.text = f'{sentimentTweet} sentiment'

            sm.current = 'tweet'

    pass

class TweetScreen(Screen):

    def goBackScreen(self):
        sm.current = 'menu'  

    def postTweet(self):
        tweet = self.ids.tweet_generated.text
        sentimentTweet = self.ids.tweet_sentiment.text
        
        if tweet == '' or tweet == 'No Tweet Generated':
            popup = Popup(title='Tweet Could Not Be Posted',
            content=Label(text='Tweet cant be blank'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        elif sentimentTweet == 'Negative sentiment':
            popup = Popup(title='Tweet Could Not Be Posted',
            content=Label(text='Tweet cant be negative'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        else:
            
            text = 'this a test tweet: ' + tweet
            #post status to twitter
            api.postStatus(text)
            popup = Popup(title='Tweet Posted',
            content=Label(text='The Tweet was posted successfully'),
            size_hint=(None, None), size=(400, 400))
            popup.open()


    pass

class MainApp(MDApp):

    def build(self):
        #Add screens to ScreenManager
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TweetScreen(name='tweet'))

        return sm

if __name__ == '__main__':
    MainApp().run()