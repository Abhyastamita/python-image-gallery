import logging
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import uuid
import os

def get_access_key_id():
    idfile = open(os.getenv("AWS_ACCESS_KEY_ID_FILE"), "r") 
    id = idfile.readline()
    idfile.close()
    return id[:-1]

def get_access_key_secret():
    secretfile = open(os.getenv("AWS_SECRET_ACCESS_KEY_FILE"), "r") 
    secret = secretfile.readline()
    secretfile.close()
    return secret[:-1]

s3_client = boto3.client('s3', aws_access_key_id=get_access_key_id(), aws_secret_access_key=get_access_key_secret())
bucket = os.getenv("S3_IMAGE_BUCKET")

def upload_image(file, owner, mime):
    img_id = str(uuid.uuid4())
    data = file
    # name = secure_filename(file)
    try:
        response = s3_client.put_object(Key=owner + "/" + img_id, Body=data, Bucket=bucket, ContentType=mime) # Metadata={'title': name})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_images(owner):
    images = s3_client.list_objects_v2(Bucket=bucket, Prefix=owner)
    path = 'gallery/ui/static/img_cache/'
    if not os.path.exists(os.path.dirname(path + owner + "/")):
        os.makedirs(os.path.dirname(path + owner + "/"))
    filenames = []
    if 'Contents' in images:
        for img in images['Contents']:
            if not  os.path.isfile(path + img['Key']):
                obj = s3_client.download_file(Bucket=bucket, Key=img['Key'], Filename=path + img['Key'])
            filenames.append(img['Key'])
    return filenames

def delete_image(filename):
    path = 'gallery/ui/static/img_cache/'
    os.remove(path + filename)
    response = s3_client.delete_object(Bucket=bucket, Key=filename)
    return response
