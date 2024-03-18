import json
import boto3

def lambda_handler(event, context):
    request_body = event['body']
    request_json = json.loads(request_body)
    
    email = request_json['email']
    password = request_json['password']
    
    cognito = boto3.client('cognito-idp')
    try:
        response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            },
            ClientId='{{COGNITO_CLIENT_ID}}'
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'access_token': response['AuthenticationResult']['AccessToken']})
        }
    except cognito.exceptions.NotAuthorizedException:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Unauthorized'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }