import os
import boto3
import epsagon
import json
import logging
import requests
import stripe
import watchtower

from flask import Flask, request, abort

logs_session = boto3.Session(
    region_name=os.environ.get('AWS_REGION'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)

epsagon.init(
    token=os.environ.get('EPSAGON_KEY'),
    app_name='order_app',
    metadata_only=False
)

app = Flask(__name__)
epsagon.flask_wrapper(app)

logging.basicConfig(level=logging.INFO)
handler = watchtower.CloudWatchLogHandler(boto3_session=logs_session)
app.logger.addHandler(handler)
logging.getLogger("werkzeug").addHandler(handler)


@app.route('/process_order', methods = ['POST'])
def process_order():
    order_payload = None
    try:
        order_payload = json.loads(request.data)
    except Exception as e:
        app.logger.error(f'Unable to parse payload {request.data}')
        app.logger.error(e)
        abort(400)

    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in order_payload:
        try:
            requests.get(order_payload.get('SubscribeURL'))
        except Exception as e:
            app.logger.error(f'Unable to confirm subscription')
            app.logger.error(e)
            abort(500)


    if order_payload is None:
        app.logger.info('No payload received')
        return 'No payload received', 200

    app.logger.info(f'Processing payment with {order_payload}')

    try:
        # generate a dummy payment intent
        stripe.api_key = os.environ.get('STRIPE_API_KEY')

        stripe.PaymentIntent.create(
            amount=json.loads(order_payload.get('Message')).get('amount'),
            currency='usd',
            payment_method_types=['card']
        )

        return 'Payment processed', 200
    except Exception as e:
        app.logger.error(f'Unable to process the payment')
        app.logger.error(e)
        abort(500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
