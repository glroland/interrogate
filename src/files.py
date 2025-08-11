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

    s3 = None

    def __init__(self):
        """ Initialize the component
        """
        self.s3 = boto3.client('s3',
                               endpoint_url=self.OBJECT_URL,
                               aws_access_key_id=self.OBJECT_ACCESS_KEY,
                               aws_secret_access_key=self.OBJECT_SECRET_KEY)

    def validate_paramters(self, username: str, path: str = None):
        """ Validates the provided input parameters for content and security.
        
            username - username
            path - requested path
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
        if path is not None and ".." in path:
            msg = f"Relative paths are not permitted.  Path={path}"
            logger.erorr(msg)
            raise ValueError(msg)

    def build_path(self, username: str, path: str = None):
        """ Build's the absolute path from the reletaive path provided.
        
            username - username
            path - requested path
        """
        # build directory name for user
        username_prefix = username + "/"
        directory = username_prefix
        if path is not None:
            directory += path
        
        logger.debug("Resulting Path from Build: Username=%s Path=%s Directory=%s UNP=%s",
                     username, path, directory, username_prefix)
    
        return directory, username_prefix

    def list(self, username: str, subdir: str = None) -> List[str]:
        """ List the files in the specified directory.
        
            username - whose home directory to search
            subdir - sub directory
        """
        # validate parameters
        self.validate_paramters(username, subdir)

        # build directory name for user
        directory, username_prefix = self.build_path(username, subdir)

        results: List[str] = []
        try:
            response = self.s3.list_objects_v2(Bucket=self.FILE_BUCKET, Prefix=directory)

            if 'Contents' in response:
                for obj in response['Contents']:
                    # Filter out the "directory" itself if it appears as an object
                    if obj['Key'] != directory:
                        filename = obj['Key']
                        filename = filename[len(username_prefix) :]
                        results.append(filename)

        except Exception as e:
            msg = f"Caught exception while listing files in Object Storage for user.  User={username}. Dir={directory}  Bucket={self.FILE_BUCKET} Exception={e}"
            logger.error(msg)
            raise ValueError(msg)

        # summarize results
        logger.info("%s results found for user %s (Dir=%s)", len(results), username, subdir)
        logger.debug("All Results - %s", results)

        return results

    def retrieve_file(self, username: str, file: str = None):
        """ Retrieve's the specified file from the object store.
         
            username - username
            file - file with subpath attached (as user sees)
            
            Returns: file contents
        """
        # validate parameters
        self.validate_paramters(username, file)

        # build directory name for user
        abs_path = self.build_path(username, file)

        contents = None
        try:
            response = self.s3.get_object(Bucket=self.FILE_BUCKET, Key=abs_path)
            contents = response['Body'].read().decode('utf-8')  # Decode if it's a text file
        except self.s3.exceptions.NoSuchKey:
            msg = f"File not found in path!  File={file} AbsPath={abs_path} Bucket={self.FILE_BUCKET}"
            logger.error(msg)
            raise ValueError(msg)
        except Exception as e:
            msg = f"Unexpected error when retrieving file!  File={file} AbsPath={abs_path} Bucket={self.FILE_BUCKET}"
            logger.error(msg)
            raise ValueError(msg)

        return contents
