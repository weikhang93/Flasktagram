import boto3
import os
import braintree


s3=boto3.client("s3",
                aws_access_key_id=os.environ.get("S3_ACCESS_ID"),
                aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"))



def upload_file_to_s3(file, username, acl="public-read"): #username is for folder creation , jw's gist don't have it
    try:
        s3.upload_fileobj(
            file,  # our image file object
            os.environ.get("S3_BUCKET"), # the bucket that we want to uplaod to
            f'{username}/{file.filename}', # pathway  to upload to s3 bucket
            ExtraArgs={
                "ACL": acl, #without setting ACL to public-read, only i can view it when i am logged into my aws.
                "ContentType": file.content_type   # it stop us from downloading it when i key in the url in the browser.
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return f'{username}/{file.filename}'




gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("BRAINTREE_MERCHANT_ID"),
        public_key=os.environ.get("BRAINTREE_PUBLIC_KEY"),
        private_key=os.environ.get("BRAINTREE_PRIVATE_KEY")
    )
)



        
