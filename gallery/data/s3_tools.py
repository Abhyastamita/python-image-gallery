import logging
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import uuid

s3_client = boto3.client('s3')

def upload_image(file, owner):
    img_id = str(uuid.uuid4())
    data = open(file, 'rb')
    name = secure_filename(file)
    try:
        response = s3_client.put_object(Key=owner + "/" + img_id, Body=data, Bucket='auburn.image-gallery', ContentType='img/jpg', Metadata={'title': name})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_images(owner):
    images = s3_client.list_objects_v2(Bucket='auburn.image-gallery', Prefix=owner)
    for img in images['Contents']:
        print(img['Key'])