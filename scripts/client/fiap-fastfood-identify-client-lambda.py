import json
import boto3

def lambda_handler(event, context):
    username = event['rawPath'].split('/')[-1]
    cognito = boto3.client('cognito-idp')

    try:
        response = cognito.admin_get_user(
            UserPoolId='{{USER_POOL_ID}}',
            Username=username
        )

        user_attributes = response['UserAttributes']
        
        user_data = {}
        for attribute in user_attributes:
            if attribute['Name'].startswith("custom:"):
                user_data[attribute['Name'].replace("custom:", "")] = attribute['Value']
            else:
                user_data[attribute['Name']] = attribute['Value']

        return {
            'statusCode': 200,
            'body': json.dumps(user_data)
        }
    except cognito.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Usuário não encontrado'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }