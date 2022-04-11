from logging import root
from tracemalloc import start
from turtle import left
from typing import Text
import kivymd
from matplotlib.style import use
import Load_Sentiment as sentiment
import Load_Generation as generate
import preview as preview
import Twitter_API as api
import myfirebase
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

# Create the properties for the generated text, and the localId and ID Token
tweetText = ''
localId = "no id"
idToken = "no id"

# Function for creating a preview using the generated tweet
def newPreview(generatedTweet):

    #Trys to get the logged in user's name and username from firebase to create the preview
    try:
        requestRefresh, id_token, local_id = myfirebase.tryRefresh()
        result = requests.get("https://deepsocial-7fb43-default-rtdb.europe-west1.firebasedatabase.app/" + local_id + ".json?auth=" + id_token)
        data = json.loads(result.content.decode())

        print(data)
    
        preview.createPreview(generatedTweet, data['name'], data['username'])
        return
    
    #If a users name cannot be gotten set name and username to default
    except:
        print("could not get data")
        preview.createPreview(generatedTweet, 'Default Name', 'Default Username')
        return

# Declare Screens
class MenuScreen(Screen):
    
    # Creating properties for the tweet, generated tweet and sentimen tweet
    tweet = ObjectProperty(None)
    generatedTweet = ObjectProperty(None)
    sentimentTweet = ObjectProperty(None)

    # Function for a user logging out
    def logout(self):
        #Clear refresh token and go back to login screen
        with open("refreshToken.txt", "w")as f:
                f.write('')
        sm.current = 'login'
        
    # Function to Reset Screeen
    def resetScreen(self):
        # Resets the tweet to blank
        tweet = self.ids.tweet.text

        # If the tweet is already blank display a popup else set the tweet to blank
        if tweet == '':
            popup = Popup(title='Tweet Could Not Be Reset',
            content=Label(text='Tweet was has nothing to reset'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        else:
            self.ids.tweet.text = ''   

    # Function to generate tweet and detect sentiment of tweet and go to tweet screen
    def pressed(self):
        # Get the tweet from the search
        tweet = self.ids.tweet.text
        
        # If the tweets is blank display a pop up
        if tweet == '':
            popup = Popup(title='Tweet Could Not Be Submitted',
            content=Label(text='Tweet cant be blank'),
            size_hint=(None, None), size=(400, 400))
            popup.open()

        # Else continue with the inputted tweet
        else:
            #Set space for rest of generated tweet
            tweetText = tweet + ' '

            #Generate a tweet and detect the sentiment of the generated tweet
            generatedTweet = generate.generateTweet(tweetText)
            sentimentTweet = sentiment.predict(generatedTweet)

            #Get the tweet screen and set the generated tweet text and sentiment text, to what was generated
            tweetScreen = self.manager.get_screen("tweet")
            tweetScreen.ids.tweet_generated.text = f'{generatedTweet}'
            tweetScreen.ids.tweet_sentiment.text = f'{sentimentTweet} sentiment'

            #Move to tweet screen
            sm.current = 'tweet'

class TweetScreen(Screen):

    #Create a preview of a tweet
    def previewTweet(self):
        #Get the generated tweet and use the new preview function discussed earlier to create a tweet
        generatedTweet = self.ids.tweet_generated.text

        newPreview(generatedTweet)

        # Get the preview screen and set the image to the tweet.png image 
        # and reload this image as if you dont the first image it makes will be used each time
        previewScreen = self.manager.get_screen("preview")
        previewScreen.ids.tweet_preview.source = 'tweet.png'
        previewScreen.ids.tweet_preview.reload()

        #Set the current screen to preview
        sm.current = 'preview'  

    def logout(self):
        with open("refreshToken.txt", "w")as f:
                f.write('')
        sm.current = 'login'
    
    #Function to go back to the menu
    def goBackScreen(self):
        sm.current = 'menu'  

    #Function to post the generated tweet
    def postTweet(self):
        #Get the generated tweet and its sentiment
        tweet = self.ids.tweet_generated.text
        sentimentTweet = self.ids.tweet_sentiment.text
        
        #If there is no tweet generated then display a popup
        if tweet == '' or tweet == 'No Tweet Generated':
            popup = Popup(title='Tweet Could Not Be Posted',
            content=Label(text='Tweet cant be blank'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        #If the sentiment is negative display a popup
        elif sentimentTweet == 'Negative sentiment':
            popup = Popup(title='Tweet Could Not Be Posted',
            content=Label(text='Tweet cant be negative'),
            size_hint=(None, None), size=(400, 400))
            popup.open()
        
        #Else post the tweet 
        else:
            #I will show that this is only a test tweet
            text = 'this a test tweet: ' + tweet
            # then use the Twitter API to post the tweet and display a popup saying it successfully posted the tweet
            api.postStatus(text)
            popup = Popup(title='Tweet Posted',
            content=Label(text='The Tweet was posted successfully'),
            size_hint=(None, None), size=(400, 400))
            popup.open()


    pass

#Login screen
class LoginScreen(Screen):

    #URL for the database
    firebaseUrl = "https://deepsocial-7fb43-default-rtdb.europe-west1.firebasedatabase.app/"
    #Token for the firebase
    webApi = "AIzaSyDQVwCqEr5N4Mj14Ie6iSIWcI7n2HAuZlI" 
    
    #When a user enters a email and password try to sign this user into firebase
    def SignIn(self, email, password):
        #get the firebase signin url
        signinUrl = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.webApi
        #set the payload and make a post request using this information
        signinPayload = {"email": email, "password": password, "returnSecureToken": True}
        signinRequest = requests.post(signinUrl, data=signinPayload)
        signinData = json.loads(signinRequest.content.decode())

        #If the request was ok set the new refresh token and go to the menu screen
        if signinRequest.ok == True:
            refreshToken = signinData['refreshToken']
            localID = signinData["localId"]
            idToken = signinData["idToken"]

            with open("refreshToken.txt", "w")as f:
                f.write(refreshToken)

            sm.current = 'menu'

        #If the request wasnt ok display a pop up saying that the user could not signin nad the reason why
        elif signinRequest.ok == False:
            err = signinData["error"]["message"]
            popup = Popup(title='Could Not Signup',
            content=Label(text=err.replace("_", " ")),
            size_hint=(None, None), size=(400, 400))
            popup.open()

    #Go to the signup screen
    def SignUp(self):
        sm.current = 'signup'  

class SignupScreen(Screen):
    firebaseUrl = "https://deepsocial-7fb43-default-rtdb.europe-west1.firebasedatabase.app/"

    webApi = "AIzaSyDQVwCqEr5N4Mj14Ie6iSIWcI7n2HAuZlI" 

    #Go to the login screen
    def SignIn(self):
        sm.current = 'login'

    #function for signingup the user through firebase given email, password, name and username
    def SignUp(self, email, password, name, username):

        #If the name/username is blank display that the name can't be blank
        if name == '':
            self.ids.signupMessage.text = 'Name can\'t be blank'
            return
        
        if username == '':
            self.ids.signupMessage.text = 'Username can\'t be blank'
            return


        signinUrl = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.webApi

        signupPayload = {"email": email, "password": password, "returnSecureToken": True}

        #Post data to the authentication
        signupRequest = requests.post(signinUrl, data = signupPayload )
        signupData = json.loads(signupRequest .content.decode())

        #If the request isnt ok display a popup with the reason why it failed
        if(signupRequest.ok == False):
            err = signupData["error"]["message"]

            if(err == "EMAIL_EXISTS"):
               
                popup = Popup(title='Could Not Signup',
                content=Label(text='User with this email already exists!'),
                size_hint=(None, None), size=(400, 400))
                popup.open()
            
            else:
                popup = Popup(title='Could Not Signup',
                content=Label(text=err.replace("_", " ")),
                size_hint=(None, None), size=(400, 400))
                popup.open()

        #Else if the request is ok signup the user
        else:
            self.ids.signupMessage.text = ""
            refreshToken = signupData["refreshToken"]
            localID = signupData["localId"]
            idToken = signupData["idToken"]

            #Save refresh Tokem
            with open("refreshToken.txt", "w")as f:
                f.write(refreshToken)

            #Save email, username and name to the database
            myData = '{"email" : \"' + email + '\" , "name" : \"' + name + '\" , "username" : \"' + username + '\" }'

            #Send data to database
            postData = requests.patch(self.firebaseUrl + localID + ".json?auth=" + idToken, data=myData)

            #Go to menu
            sm.current = 'menu'  

    pass

class PreviewScreen(Screen):
    
    def logout(self):
        with open("refreshToken.txt", "w")as f:
                f.write('')
        sm.current = 'login'

    def goBackScreen(self):
        sm.current = 'tweet'  

    def postTweet(self):
        tweetScreen = self.manager.get_screen("tweet")
        tweet = tweetScreen.ids.tweet_generated.text
        sentimentTweet = tweetScreen.ids.tweet_sentiment.text

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

class MainApp(MDApp):

    #Build the kivy application
    def build(self):
        #Add screens to ScreenManager
        self.theme_cls.secondary_palette = "Red"
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TweetScreen(name='tweet'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(PreviewScreen(name='preview'))
        sm.add_widget(SignupScreen(name='signup'))

        #Try logging in the user
        try:
            requestRefresh, id_token, local_id = myfirebase.tryRefresh()
            #If the user was previsouly logged in go to menu else go to the login screen
            if(requestRefresh == True):
                sm.current = 'menu'
            
            else:
                sm.current = 'login'

        except:
            sm.current = 'login'
            
        return sm

if __name__ == '__main__':
    MainApp().run()


