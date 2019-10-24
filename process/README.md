# Process Order API

The **Process Order API** is a very small API (one endpoint) written with the Flask Framework (Python 3.7). The `/process_order` endpoint acts as a callback of the SNS subscription. So when the order app post a message to the SNS topic, the endpoint procceses the actual order. The endpoint asumes there will be always enough stock and thus it generates a payment´s intent.

## How to run it?

### Requirements

1. AWS credentials.
2. SNS topic already created.
3. An email´s subscription to the topic.
4. Epsagon API Key.
5. Stripe API Key

### Virtual environment - Local - Flask development server

1. `pip install virtualenv`
2. `virtualenv env --python=python3.7`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `AWS_ACCESS_KEY=<your_aws_access_key> AWS_SECRET_ACCESS_KEY=<your_aws_secret_key> AWS_REGION=<deployed_region> STRIPE_API_KEY=<your_stripe_api_key> EPSAGON_KEY=<your_epsagon_key> FLASK_APP=app.py flask run`

POST http://localhost:5000/process_order

`
{
    "Message": {
        "order": "1",
        "product": "Echo Dot (2nd Generation)",
        "amount": 400
    }
}
`
### Virtual environment - Local - Gunicorn

1. `pip install virtualenv`
2. `virtualenv env --python=python3.7`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `AWS_ACCESS_KEY=<your_aws_access_key> AWS_SECRET_ACCESS_KEY=<your_aws_secret_key> AWS_REGION=<deployed_region> STRIPE_API_KEY=<your_stripe_api_key> EPSAGON_KEY=<your_epsagon_key> gunicorn --bind 0.0.0.0:8000 wsgi:app`

POST http://localhost:8000/process_order

`
{
    "Message": {
        "order": "1",
        "product": "Echo Dot (2nd Generation)",
        "amount": 400
    }
}
`

### Docker - Local - Gunicorn

1. `docker build -t <your-repo>/process_order .`
2. `docker run -p 8000:8000 -e AWS_ACCESS_KEY=<your_aws_access_key> -e AWS_SECRET_ACCESS_KEY=<your_aws_secret_key> -e AWS_REGION=<deployed_region> -e STRIPE_API_KEY=<your_stripe_api_key> -e EPSAGON_KEY=<your_epsagon_key> --rm <your-namespace>/process_order`

POST http://<your_local_ip>:8000/process_order
`
{
    "Message": {
        "order": "1",
        "product": "Echo Dot (2nd Generation)",
        "amount": 400
    }
}
`

### Docker - AWS - Gunicorn - Fargate (Use your own zone)

1. Create a repository on AWS ECR (https://us-east-1.console.aws.amazon.com/ecr/get-started)
2. Get authenticated against AWS $(aws ecr get-login --no-include-email --region us-east-1)
3. `docker tag <your-repo>:process_order_app <owner_id>.dkr.ecr.us-east-1.amazonaws.com/<your_repo>:latest`
4. `docker push <owner_id>.dkr.ecr.us-east-1.amazonaws.com/<your_repo>:process_order_app`
5. Create a task definition and run it following https://epsagon.com/blog/deploying-java-spring-boot-on-aws-fargate/
6. Hit the endpoint

POST http://<AWS_FARGATE_IP>:8000/process_order

`
{
    "Message": {
        "order": "1",
        "product": "Echo Dot (2nd Generation)",
        "amount": 400
    }
}
`

### Connecting the SNS subscription with the endpoint

Once you get the public IP provided by AWS Fargate, you can create an HTTP subscription. By adding the IP and port you will connect both applications (order_app, process_order_app) in a publisher / consumer fashion.

In all cases, you should see payments created on the Stripe dashboard.