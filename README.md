# Orders API

The **demo-retail-app** is a very small API (one endpoint) written with the Flask Framework (Python 3.7). The `/order` endpoint receives an order´s payload and it publishes a message on a SNS topic, so that a consumer can process the request later on.

## How to run it?

### Requirements

1. AWS credentials.
2. SNS topic already created.
3. An email´s subscription to the topic.
4. Epsagon Key.

### Virtual environment - Local - Flask development server

1. `pip install virtualenv`
2. `virtualenv env --python=python3.7`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `AWS_ACCESS_KEY=<your_aws_access_key> AWS_SECRET_ACCESS_KEY=<your_aws_secret_key> AWS_REGION=<deployed_region> APP_TOPIC=<sns_topic> EPSAGON_KEY=<your_epsagon_key> FLASK_APP=app.py flask run`

POST http://localhost:5000/order

`
{
 "order": "1",
 "product": "Echo Dot (2nd Generation)",
 "amount": 400
}
`
### Virtual environment - Local - Gunicorn

1. `pip install virtualenv`
2. `virtualenv env --python=python3.7`
3. `source env/bin/activate`
4. `pip install -r requirements.txt`
5. `AWS_ACCESS_KEY=<your_aws_access_key> AWS_SECRET_ACCESS_KEY=<your_aws_secret_key> AWS_REGION=<deployed_region> APP_TOPIC=<sns_topic> EPSAGON_KEY=<your_epsagon_key> gunicorn --bind 0.0.0.0:8000 wsgi:app`

POST http://localhost:8000/order

`
{
 "order": "1",
 "product": "Echo Dot (2nd Generation)",
 "amount": 400
}
`
### Docker - Local - Gunicorn

1. `docker build -t <your-repo>/order_app  .`
2. `docker run -p 8000:8000 -e AWS_ACCESS_KEY=<your_aws_access_key> -e AWS_SECRET_ACCESS_KEY=<your_aws_secret_key> -e AWS_REGION=<deployed_region> -e APP_TOPIC=<sns_topic> -e EPSAGON_KEY=<your_epsagon_key> --rm <your-repo>/order_app`

POST http://<your_local_ip>:8000/order

`
{
 "order": "1",
 "product": "Echo Dot (2nd Generation)",
 "amount": 400
}
`

### Docker - AWS - Gunicorn - Fargate (Use your own zone)

1. Create a repository on AWS ECR (https://us-east-1.console.aws.amazon.com/ecr/get-started)
2. Get authenticated against AWS $(aws ecr get-login --no-include-email --region us-east-1)
3. `docker tag <your-repo>:order_app <owner_id>.dkr.ecr.us-east-1.amazonaws.com/<your_repo>:latest`
4. `docker push <owner_id>.dkr.ecr.us-east-1.amazonaws.com/<your_repo>:order_app`
5. Create a task definition and run it following https://epsagon.com/blog/deploying-java-spring-boot-on-aws-fargate/
6. Hit the endpoint

POST http://<AWS_FARGATE_IP>:8000/order

`
{
 "order": "1",
 "product": "Echo Dot (2nd Generation)",
 "amount": 400
}
`

In all cases, you should see the payload sent to the endpoint on your email´s inbox.
