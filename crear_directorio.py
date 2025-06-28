import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        # Parse the request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
            
        bucket_name = body.get('bucket_name')
        directory_name = body.get('directory_name')
        
        if not bucket_name or not directory_name:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'El nombre del bucket y el directorio son requeridos'
                })
            }
        
        # Ensure directory name ends with '/'
        if not directory_name.endswith('/'):
            directory_name += '/'
        
        # Create S3 client
        s3_client = boto3.client('s3')
        
        # Create the directory by uploading an empty object
        s3_client.put_object(
            Bucket=bucket_name,
            Key=directory_name,
            Body=''
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Directorio {directory_name} creado exitosamente en el bucket {bucket_name}'
            })
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al crear el directorio: {str(e)}'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error inesperado: {str(e)}'
            })
        }
