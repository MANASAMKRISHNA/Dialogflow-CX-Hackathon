from flask import Flask, request, jsonify
from twilio.rest import Client
import requests
import json

client_msg = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')

app = Flask(__name__)

def phone_number():
    global ph_no
    ph_no=request.json['sessionInfo']['parameters']['phone-number']
    print("Phone number : ", ph_no)

def search_by_city():
    global response_data
    city=request.json['sessionInfo']['parameters']['city']
    url = "https://us-real-estate.p.rapidapi.com/v2/for-rent"
    querystring = {"city":city,"state_code":"CA"}
    headers = {
        'x-rapidapi-host': "us-real-estate.p.rapidapi.com",
        'x-rapidapi-key': "Rapid API key"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_data = json.loads(response.text)
    response_data=response_data['data']['home_search']['results']
    print("Number of available apartments in " + city +" is ", len(response_data))
    
def search_by_zipcode():
    global response_data
    zipcode=request.json['sessionInfo']['parameters']['zipcode']
    zipcode=str(zipcode)
    url = "https://us-real-estate.p.rapidapi.com/v2/for-rent"
    querystring = {"location":zipcode,"state_code":"CA"}
    headers = {
        'x-rapidapi-host': "us-real-estate.p.rapidapi.com",
        'x-rapidapi-key': "Rapid API Key"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_data = json.loads(response.text)
    response_data=response_data['data']['home_search']['results']
    print("Number of available apartments in " + zipcode +" is ", len(response_data))


    
def no_of_bedrooms():
    global filtered_results
    filtered_results=[]
    count=0
    bedrooms=request.json['sessionInfo']['parameters']['bedrooms']
    bedrooms=str(bedrooms)
    print("Number of bedrooms ", bedrooms)
    for i in response_data:
        if(bedrooms=='any'):
            count=count+1
            filtered_results.append(i)
        elif(str(i['description']['beds_max'])==bedrooms):
                count=count+1
                filtered_results.append(i)

    print("Number of apartments with bedroom filter ", str(count))
    
def max_rent():
    count=0
    max_rent=request.json['sessionInfo']['parameters']['max-rent']
    max_rent=max_rent['amount']
    print("Desired maximum rent ", max_rent)
    for i in list(filtered_results):
        if(str(i['list_price_max'])<=str(max_rent)):
            count=count+1
        else:
            filtered_results.remove(i)

    print("Number of apartments with rent filter  ",str(count))
    
def no_of_bathrooms():
    count=0
    bathrooms=request.json['sessionInfo']['parameters']['bathrooms']
    bathrooms=str(int(bathrooms))
    print("Number of bathrooms ", bathrooms)
    for i in list(filtered_results):
        if(bathrooms=='any'):
            count=count+1
        elif(str(i['description']['baths_max'])==bathrooms):
            count=count+1
        else:
            filtered_results.remove(i)

    print("Number of apartments with bathroom filter ", str(count))

def pets_policy():
    count=0
    pets=request.json['sessionInfo']['parameters']['pets']
    pets=str(pets)
    print("Pets ", pets)
    for i in list(filtered_results):
        if(pets=='yes'):
            if('pets_allowed' in i['tags']):
                count=count+1
            else:
                filtered_results.remove(i)
        else:
            count=count+1
    print("Number of apartments with pets policy ", str(count))

def filter_by_no_of_bedrooms():
    #Filter out the API results based on the number of bedrooms 
    no_of_bedrooms()
    #If there are no available apartments give the option of starting over or changing the search criteria.
    count=len(filtered_results)
    if(count==0):
        text='Oops! Looks like there are no available apartments with the preferred requirements. You can either change the search criteria or you can start over. How would you like to continue?'

    else:
        text='Perfect! So far I have found '+ str(count) +' apartments for you. Would you like to narrow your search further by selecting your desired maximum rent? Please say "yes" or "no".'
    fulfillmentResponse = {
        'fulfillment_response': {
            'messages': [{
                'text': {
                    'text':[text]
                }
            }]
        }
    }
    return fulfillmentResponse

def filter_by_max_rent():
    #Filter out the API results based on the number of bedrooms and max rent
    no_of_bedrooms()
    max_rent()
    #If there are no available apartments give the option of starting over or changing the search criteria.
    count=len(filtered_results)
    if(count==0):
        text= 'Oops! Looks like there are no available apartments with the preferred requirements. You can either change the search criteria or you can start over. How would you like to continue?'

    else:
        text = 'Perfect! So far I have found '+ str(count) +' apartments for you. Would you like to narrow your search further by selecting preffered number of bathrooms? Please answer yes or no.'
    fulfillmentResponse = {
        'fulfillment_response': {
            'messages': [{
                'text': {
                    'text': [text]
                }
            }]
        }
    }
    return fulfillmentResponse

def filter_by_no_of_bathrooms():
    #Filter out the API results based on the number of bedrooms, max rent and bathrooms
    no_of_bedrooms()
    max_rent()
    no_of_bathrooms()
    #If there are no available apartments give the option of starting over or changing the search criteria.
    count=len(filtered_results)
    if(count==0):
        text= 'Oops! Looks like there are no available apartments with the preferred requirements. You can either change the search criteria or you can start over. How would you like to continue?'

    else:
        text = 'Perfect! So far I have found '+ str(count) +' apartments for you. Would you like to narrow your search further by pets policy? Please answer yes or no.'
    fulfillmentResponse = {
        'fulfillment_response': {
            'messages': [{
                'text': {
                    'text': [text]
                }
            }]
        }
    }
    return fulfillmentResponse

def filter_by_pets_policy():
    #Filter out the API results based on the number of bedrooms, max rent, bathrooms and pets policy
    no_of_bedrooms()
    max_rent()
    no_of_bathrooms()
    pets_policy()
    
def send_sms():
    #If there are no available apartments give the option of starting over or changing the search criteria.
    if (len(filtered_results)==0):
        text='Oops! Looks like there are no available apartments with the preferred requirements. You can either change the search criteria or you can start over. How would you like to continue?'

    else:
        #send text mesage with available apartments
        j=0
        message="Hello!\nI am glad to let you know that I found some prefect apartments for you.\n"
        for i in filtered_results:
            j=j+1
            message=message +'\n'+ (i['advertisers'][1]['office']['name'])  +'\nLeasing ID  ' + str(i['listing_id']) + '\nSquare Footage  ' + str(i['description']['sqft_max'])+ '\nMonthly Rent  '+str(i['list_price_max'])+'\nBedroom  '+str(i['description']['beds_max'])+'\nContact Number ' + str(i['advertisers'][1]['office']['phones'][0]['number']) +'.\n'
            #Limit the number of available apartments to 7
            if(j>9):
                break
        print(message)
        
        msg = client_msg.messages.create(
              body=message,
              from_='Twilio Phone number',
              to=ph_no
          )
        print("Message sent successfully")
        text='Please hold for a brief moment I send you a text message with few apartment choices with Property Name, Leasing ID, Monthly Rent, Square Footage and contact number. Please confirm when you receive a text message.'
    fulfillmentResponse = {
        'fulfillment_response': {
            'messages': [{
                'text': {
                    'text': [text]
                }
            }]
        }
    }
    return fulfillmentResponse
    



def webhook():
    req = request.get_json(force=True)
    #print(req)
    session_id = request.json['sessionInfo']['session'].split('/')[-1] 
    print("session_id : "+ session_id)
    tag = request.json['fulfillmentInfo']['tag']
    print(request.json['sessionInfo']['parameters'])
    print("tag:"+ tag)
    
    #Match and call the corresponding tag
    if(tag=='phone_number'):
        phone_number()
        
    if(tag=='search-by-city'):
        search_by_city()
        
    if(tag=='search-by-zipcode'):
        search_by_zipcode()
        
    if(tag=='filter-by-no-of-bedrooms'):
        resp=filter_by_no_of_bedrooms()
        return jsonify(resp)
    
    if(tag=='filter-by-max-rent'):
        resp=filter_by_max_rent()
        return jsonify(resp)
    
    if(tag=='filter-by-no-of-bathrooms'):
        resp=filter_by_no_of_bathrooms()
        return jsonify(resp)
    
    if(tag=='filter-by-pets-policy'):
        filter_by_pets_policy()   
        
    if(tag=='send-sms'):
        resp=send_sms()
        return jsonify(resp)

@app.route('/webhook', methods=['GET', 'POST'])

def index():
    print('index')
    return webhook()
        
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    #app.run()