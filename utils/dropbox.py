from django.core.management.base import NoArgsCommand
from dropbox import rest, session
# from django_dropbox.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TYPE
from django.conf import settings
from datetime import datetime
import dropbox
import glob, os

_now = datetime.now()
_local = '/RootAir/%s/%s/%s/' %(_now.year, _now.month, _now.day)

def remove_file_dropbox(_file):
    """
    :param _file:
    :return:
    """
    try:
        _local_file = _local + _file
        client_dropbox().file_delete(_local_file)
    except:
        pass

def send_file_dropbox(_file):
    """
    :param _file:
    :return:
    """
    try:
        _local_file = _local  +  _file.file.name.split('/')[-1]
        _response = client_dropbox().put_file(_local_file, _file)
        return settings.URL_DROPBOX + _response['path']
    except:
        return _file

def get_file_dropbox(_file):
    """
    :param _file:
    :return:
    """
    try:
        _file = _file.name.replace(settings.URL_DROPBOX,'').replace('?preview=','/')
        f = client_dropbox().get_file(_file)
        return f
    except:
        return False

def client_dropbox():
    """
    :return:
    """
    client = dropbox.client.DropboxClient(settings.DROPBOX_ACCESS_TOKEN)
    return client

class Command(NoArgsCommand):
    """
    """
    CACHE_TIMEOUT = getattr(settings, 'DROPBOX_CACHE_TIMEOUT', 3600 * 24 * 365)   # One year
    # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
    ACCESS_TYPE = 'dropbox'

    def handle_noargs(self, *args, **options):
        fflow = dropbox.client.DropboxOAuth2FlowNoRedirect(DROPBOX_CONSUMER_KEY, DROPBOX_CONSUMER_SECRET)
        # Have the user sign in and authorize this token
        authorize_url = flow.start()
        print('1. Go to: ' + authorize_url)
        print('2. Click "Allow" (you might have to log in first)')
        print('3. Copy the authorization code.')
        code = raw_input("Enter the authorization code here: ").strip()

        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)

        # sess = session.DropboxSession(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TYPE)
        # request_token = sess.obtain_request_token()
        #
        # url = sess.build_authorize_url(request_token)
        # print("Url:", url)
        # print("Please visit this website and press the 'Allow' button, then hit 'Enter' here.")
        # raw_input()
        # # This will fail if the user didn't visit the above URL and hit 'Allow'
        # access_token = sess.obtain_access_token(request_token)

        print( "DROPBOX_ACCESS_TOKEN = '%s'" % access_token.key)
        print( "DROPBOX_ACCESS_TOKEN_SECRET = '%s'" % access_token.secret)
