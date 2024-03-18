import json
import boto3

def lambda_handler(event, context):
    request_body = event['body']
    request_json = json.loads(request_body)
    
    email = request_json['email']
    password = request_json['password']
    cpf = request_json['cpf']
    if "name" in request_json:
        name = request_json['name']
    else:
        name = ""
    
    cognito = boto3.client('cognito-idp')
    
    try:
        response = cognito.sign_up(
            ClientId='{{COGNITO_CLIENT_ID}}',
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email}, 
                {'Name': 'name', 'Value': name}, 
                {'Name': 'custom:cpf', 'Value': cpf}
            ]
        )
        cognito.admin_confirm_sign_up(
            UserPoolId='{{USER_POOL_ID}}',
            Username=email
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Usuário cadastrado com sucesso'})
        }
    except cognito.exceptions.UsernameExistsException:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Nome de usuário já existe'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }