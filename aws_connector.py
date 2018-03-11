import boto3

# Storage
BUCKET = 'bucket-doorbell'

# upload image to bucket
s3 = boto3.client('s3')

# way back here
sqs = boto3.client('sqs')
queue = sqs.Queue('https://sqs.eu-west-1.amazonaws.com/233680902524/sqsDoorbell.fifo')
messages = queue.receive_message(WaitTimeSeconds=1)
print(messages)

#response = queue.delete_messages(
#    Entries=[
#        {
#            'Id': 'string',
#            'ReceiptHandle': 'string'
#        },
#    ]
#)

def send_image():
    print("Uploading S3 object")
    image_file = open('image.jpg', 'rb')
    s3.put_object(Bucket=BUCKET, Key='obrazek.jpg', Body=image_file)
