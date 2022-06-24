import logging
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import uuid
import os

s3_client = boto3.client('s3')

def upload_image(file, owner, mime):
    img_id = str(uuid.uuid4())
    data = file
    bucket = 'auburn.image-gallery'
    # name = secure_filename(file)
    try:
        response = s3_client.put_object(Key=owner + "/" + img_id, Body=data, Bucket=bucket, ContentType=mime) # Metadata={'title': name})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_images(owner):
    bucket = 'auburn.image-gallery'
    images = s3_client.list_objects_v2(Bucket=bucket, Prefix=owner)
    path = '/home/ec2-user/python-image-gallery/gallery/ui/static/img_cache/'
    if not os.path.exists(os.path.dirname(path + owner + "/")):
        os.makedirs(os.path.dirname(path + owner + "/"))
    filenames = []
    for img in images['Contents']:
        if not  os.path.isfile(path + img['Key']):
            obj = s3_client.download_file(Bucket=bucket, Key=img['Key'], Filename=path + img['Key'])
        filenames.append(img['Key'])
    return filenames

def delete_image(filename):
    bucket = 'auburn.image-gallery'
    path = '/home/ec2-user/python-image-gallery/gallery/ui/static/img_cache/'
    os.remove(path + filename)
    response = s3_client.delete_object(Bucket=bucket, Key=filename)
    return response
