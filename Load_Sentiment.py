import pickle
# Load the model
pickle_in = open("sentiment.pickle", "rb")
model = pickle.load(pickle_in)

def predict(tweet):
    tweet = tweet.lower()
    predictions = model.predict([tweet])
    
    #getting the prediction from the array
    prediction = predictions[0]
    return prediction