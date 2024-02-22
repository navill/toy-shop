import json

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name):
    region_name = "ap-northeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )["SecretString"]
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        return dict()

    return json.loads(get_secret_value_response)


db_secret_keys = get_secret("toy/navill/mysql")
secret_keys = get_secret("toy/navill/secret")
