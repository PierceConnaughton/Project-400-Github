from logging import root
from tracemalloc import start
from turtle import left
from typing import Text
import kivymd
import Load_Sentiment as sentiment
import Load_Generation as generate
import Twitter_API as api
import requests
import json
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
            tweetScreen.ids.tweet_generated.text = f'{generatedTweet}'
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

class LoginScreen(Screen):
    firebaseUrl = "https://deepsocial-7fb43-default-rtdb.europe-west1.firebasedatabase.app/"

    webApi = "AIzaSyDQVwCqEr5N4Mj14Ie6iSIWcI7n2HAuZlI" 

    def SignUp(self, email, password):
        signinUrl = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.webApi

        signupPayload = {"email": email, "password": password, "returnSecureToken": True}

        #Post data to the authentication
        signupRequest = requests.post(signinUrl, data = signupPayload )
        signupData = json.loads(signupRequest .content.decode())

        if(signupRequest.ok == False):
            err = signupData["error"]["message"]

            if(err == "EMAIL_EXISTS"):
               self.SignIn(email, password)
            
            else:
                self.ids.loginMessage.text = err.replace("_", " ")

        else:
            self.ids.loginMessage.text = ""
            refreshToken = signupData["refreshToken"]
            localID = signupData["localId"]
            idToken = signupData["idToken"]

            #Save refresh Tokem
            with open("refreshToken.txt", "w")as f:
                f.write(refreshToken)

            #Save email to database
            myData = '{"email" : \"' + email + '\"}'
            #Send email to database
            postData = requests.patch(self.firebaseUrl + localID + ".json?auth=" + idToken, data=myData)

            sm.current = 'menu'  

    
    def SignIn(self, email, password):
        signinUrl = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.webApi
        signinPayload = {"email": email, "password": password, "returnSecureToken": True}
        signinRequest = requests.post(signinUrl, data=signinPayload)
        signinData = json.loads(signinRequest.content.decode())

        if signinRequest.ok == True:
            refreshToken = signinData['refreshToken']
            localId = signinData['localId']
            idToken = signinData['idToken']

            with open("refreshToken.txt", "w")as f:
                f.write(refreshToken)

            sm.current = 'menu'

        elif signinRequest.ok == False:
            err = signinData["error"]["message"]
            self.ids.loginMessage.text = err.replace("_", " ")

    pass

class MainApp(MDApp):

    def build(self):
        #Add screens to ScreenManager
        self.theme_cls.secondary_palette = "Red"
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TweetScreen(name='tweet'))

        return sm

if __name__ == '__main__':
    MainApp().run()