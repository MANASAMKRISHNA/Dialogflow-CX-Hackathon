# Dialogflow-CX-Hackathon
The Voice assistant bot helps you find available apartments for rent in California. You can either search by the name of city or zip code in California. Further, you have the option to filter the results by number of bedrooms, maximum desired rent amount, number of bathrooms, pet policy. You also have the option of changing the search criteria or starting over. At the end of the  call, you will receivce a text message listing the available apartment options along with monthly rent, sqaure footage, Leasing ID, number of bed rooms and the contact number for each of the property. The text message will contain no more than 10 available apartments.

You can search for available apartments by just dialing any one of these numbers,

+1(801) 406-1372 (Dialoglfow phone gateway)

+1(747) 219-1359 (Audio Codes)

+1(306) 500-5124 (Avaya)

+1(818) 851-0982 (Voximplant)

To run the webhook.py file locally install the two below packages and use the APIs follow the below steps,
# Install Packages:

$ pip install Flask

$ pip install twilio

# API Setup

Twilio SMS API:

Set up a Twilio [account](https://www.twilio.com/try-twilio) if you don't have one. Once you have a Twilio account. Buy a phone number to send a text message to users. Update the phone number in webhook file. In Twilio console, you can also find the Twilio Account SID and Auth Token. Add these credentials in the file.

Rapid API:
Create an account in Rapid API and subscribe to this [API](https://rapidapi.com/datascraper/api/us-real-estate/). In the API console you can see code snippets. Select python -> requests. You will find the API host and key. Place these credentials in webhook file.

Aditionally, if you would like a voice bot, Integrate the bot with one of the telephony providers.



 
