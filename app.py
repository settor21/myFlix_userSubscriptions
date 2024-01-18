from flask import Flask, render_template, jsonify, request,redirect
from pymongo import MongoClient
from datetime import datetime
import stripe

app = Flask(__name__)

# Initialize MongoDB client
mongo_client = MongoClient('mongodb://35.239.170.49:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.1')
db = mongo_client['userSubscriptions']
subscription_collection_confirm = db['subscriptionConfirm']

# Set your Stripe secret key
stripe.api_key = 'sk_test_51OWM3eAf4waSqpHWwFP0YNXUMYBX3J1Wc0ybPf5ASHmufkIaa6LNJC8byZRtOKXZJ911VfRqsiSEfC3ZpkLP65iM00v1QHAGAY'

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_6nEciWXYWavBWXovYUeZln6YnEDoSV8C'

# Global variable to store user_id
current_user_id = None


@app.route('/subscribe', methods=['GET', 'POST'])
def confirm_subscription():
    if request.method == 'POST':
        data = request.get_json()
        current_user_id = data.get('user_id')
        if current_user_id:
            # Render the confirmSubscription template with user_id
            return render_template('confirmSubscription.html', user_id=current_user_id)
    elif request.method == 'GET':
        return render_template('confirmSubscription.html')


@app.route('/renew')
def renew_subscription():
    return render_template('renewSubscription.html')



@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers['Stripe-Signature']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        current_user_id = None
        # For Paid-tier, set paidSubscriber to CONFIRMED and amount to 5, and store in MongoDB
        data = {'userId': current_user_id, 'paidSubscriber': 'CONFIRMED', 'sessionID': session,
                'amount': 5, 'timestamp': datetime.now()}
        # subscription_collection_confirm.insert_one(data)
        # # Redirect to login page after successful payment

    return jsonify(success=True)





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5002)
