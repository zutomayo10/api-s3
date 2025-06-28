import json
import boto3
import base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        # Parse the request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
            
        bucket_name = body.get('bucket_name')
        file_name = body.get('file_name')
        file_content = body.get('file_content')
        directory_path = body.get('directory_path', '')
        
        if not all([bucket_name, file_name, file_content]):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'El nombre del bucket, nombre del archivo y contenido son requeridos'
                })
            }
        
        # Ensure directory path ends with '/' if it exists
        if directory_path and not directory_path.endswith('/'):
            directory_path += '/'
        
        # Decode base64 content if provided
        try:
            file_content = base64.b64decode(file_content)
        except Exception as decode_error:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'El contenido del archivo debe estar en formato base64. Error: {str(decode_error)}'
                })
            }
        
        # Create S3 client
        s3_client = boto3.client('s3')
        
        # Upload the file
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"{directory_path}{file_name}",
            Body=file_content
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Archivo {file_name} subido exitosamente a {directory_path} en el bucket {bucket_name}'
            })
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al subir el archivo: {str(e)}'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error inesperado: {str(e)}'
            })
        }
