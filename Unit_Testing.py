import unittest
import Load_Sentiment as sentiment
import Twitter_API as api
import json
import preview as preview
from PIL import Image
import Load_Generation as generate

class TestApi(unittest.TestCase):
    def test_search_tweets(self):
        """
        Test that api call for getting popular tweets based on a term is getting a dict json of tweets
        """
        data = "beach"
        result = api.getPopularTweetsTerm(data)
        self.assertIsInstance(result, dict)
    
    def test_get_timeline(self):
        """
        Test that api call for getting timeline based on a user handle is getting a list of tweets
        """
        data = "party_pierce"
        result = api.getTimeline(data)
        self.assertIsInstance(result, list)

    # def test_post_tweet(self):
    #     """
    #     Test that api call for posting a tweet returns a status that includes the text that was input
    #     """
    #     data = "test tweet"
    #     result = api.postStatus(data).text
    #     self.assertEqual(result, "test tweet")

class TestPreview(unittest.TestCase):
    def test_preview(self):
        """
        Test that the preview creates an image
        """
        result = preview.createPreview("generated tweet", 'Default Name', 'Default Username')
        self.assertIsInstance(result, Image.Image)

class TestSentiment(unittest.TestCase):
    def test_positive_sentiment(self):
        """
        Test that the sentiment is positive
        """
        data = "Good"
        result = sentiment.predict(data)
        self.assertEqual(result, 'Positive')
    
    def test_negative_sentiment(self):
        """
        Test that the sentiment is negative
        """
        data = "Bad"
        result = sentiment.predict(data)
        self.assertEqual(result, 'Negative')

    def test_neutral_sentiment(self):
        """
        Test that the sentiment is neutral
        """
        data = "Ok"
        result = sentiment.predict(data)
        self.assertEqual(result, 'Neutral')

class TestGeneration(unittest.TestCase):
    def test_generated_tweet(self):
        """
        Test that AI generates text that is longer than what was started with
        """
        data = "Hello"
        result = generate.generateTweet(data)
        self.assertGreater(result, "Hello")

if __name__ == '__main__':
    unittest.main()