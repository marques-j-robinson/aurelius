import boto3


def format_title(title):
    """
    Format painting title from object key.

    Provided with an S3 object, will extract the key and format as a title.
    """
    return title.split('.')[0].replace('-', ' ').title()


class S3:

    def __init__(self):
        """
        Initialize instance of boto3 (AWS) S3 SDK.

        This interface connects to the resource and client APIs
        """
        self.resource_api   = boto3.resource('s3')
        self.client_api     = boto3.client('s3')

    def get_objects(self, buckets):
        """
        Get objects from buckets.

        If only one bucket is provided, return the objects for that bucket.
        Otherwise, return a dictionary with the objects organized by bucket.
        """
        if type(buckets) is not list:
            # NOTE buckets is singular here
            bucket = self.resource_api.Bucket(buckets)
            return list(bucket.objects.all())
        else:
            res = {}
            for bucket_name in buckets:
                bucket = self.resource_api.Bucket(bucket_name)
                res[bucket_name] = list(bucket.objects.all())
            return res

    def delete_object(self, bucket, key):
        """
        Delete an object.

        Given a bucket and a key, delete the object.
        """
        self.resource_api.Object(bucket, key).delete()


    def rename_object(self, src, should_delete=False):
        """
        Rename an object.

        src - Needs to contain the following properties:
                new_bucket
                old_bucket
                new_key
                old_key

        should_delete(False) - Allows the user to delete the old object.
        """
        new_bucket = src['new_bucket']
        old_bucket = src['old_bucket']
        new_key = src['new_key']
        old_key = src['old_key']

        self.resource_api.Object(new_bucket, new_key).copy_from(CopySource=f'{old_bucket}/{old_key}')
        if should_delete is True:
            self.delete_object(old_bucket, old_key)

    def download_file(self, bucket, key, filename):
        """
        Download a file.

        Provide the bucket, key and filename destination.
        This function will download the object to the provided destination.
        """
        self.client_api.download_file(bucket, key, filename)
