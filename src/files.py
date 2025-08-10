import os
import logging
from typing import List
import boto3

logger = logging.getLogger(__name__)

class FileGateway:
    """ Utility class for accessing files in object storage. """

    OBJECT_URL = os.environ.get('OBJECT_URL')
    OBJECT_ACCESS_KEY = os.environ.get('OBJECT_ACCESS_KEY')
    OBJECT_SECRET_KEY = os.environ.get('OBJECT_SECRET_KEY')
    FILE_BUCKET = os.environ.get('FILE_BUCKET')

    def list(self, username: str, subdir: str = None) -> List[str]:
        """ List the files in the specified directory.
        
            username - whose home directory to search
            subdir - sub directory
        """
        # validate username - required parameter
        if username is None or len(username) == 0:
            msg = "Username is a required parameter and cannot be empty!"
            logger.error(msg)
            raise ValueError(msg)

        # validate inputs - relative paths are not allowed for security reasons
        if ".." in username:
            msg = f"Relative paths are not permitted.  Username={username}"
            logger.erorr(msg)
            raise ValueError(msg)
        if subdir is not None and ".." in subdir:
            msg = f"Relative paths are not permitted.  Subdir={subdir}"
            logger.erorr(msg)
            raise ValueError(msg)

        s3 = boto3.client('s3',
                          endpoint_url=self.OBJECT_URL,
                          aws_access_key_id=self.OBJECT_ACCESS_KEY,
                          aws_secret_access_key=self.OBJECT_SECRET_KEY)

        # build directory name for user
        username_prefix = username + "/"
        directory = username_prefix
        if subdir is not None:
            directory += subdir

        results: List[str] = []
        try:
            response = s3.list_objects_v2(Bucket=self.FILE_BUCKET, Prefix=directory)

            if 'Contents' in response:
                for obj in response['Contents']:
                    # Filter out the "directory" itself if it appears as an object
                    if obj['Key'] != directory:
                        filename = obj['Key']
                        filename = filename[len(username_prefix) :]
                        results.append(filename)

        except Exception as e:
            msg = f"Caught exception while listing files in Object Storage for user.  User={username}. Dir={directory}  Bucket={self.FILE_BUCKET}"
            logger.error(msg)
            raise ValueError(msg)

        # summarize results
        logger.info("%s results found for user %s (Dir=%s)", len(results), username, subdir)
        logger.debug("All Results - %s", results)

        return results
