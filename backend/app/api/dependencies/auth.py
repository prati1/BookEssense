from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings

# OAuth settings
GOOGLE_CLIENT_ID = settings.google_client_id or None
GOOGLE_CLIENT_SECRET = settings.google_client_secret or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing google authentication credentials. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file.')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)