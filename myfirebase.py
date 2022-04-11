import requests

#Function for when given a refresh token check to see if it can actually be used
def exchange_refresh_token(refresh_token):
        webApi = "AIzaSyDQVwCqEr5N4Mj14Ie6iSIWcI7n2HAuZlI" 
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + webApi
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        id_token = refresh_req.json()['id_token']
        local_id = refresh_req.json()['user_id']
        
        return refresh_req.ok, id_token, local_id

#function for logging into firebase
def tryRefresh():
    try:
        with open("refreshToken.txt", 'r') as f:
            refresh_token = f.read()
        
        
            requestRefresh, id_token, local_id = exchange_refresh_token(refresh_token)
            return requestRefresh, id_token, local_id
    
    except:
        pass