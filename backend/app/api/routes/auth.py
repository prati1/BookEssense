from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuthError
from app.schemas.user import UserCreate
from app.api.dependencies.auth import oauth
from app.core.logging import logger
from app.services.user import get_user_by_email, create_user
from app.db.session import get_db

router = APIRouter()

@router.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
    logger.info(redirect_uri)
    return await oauth.google.authorize_redirect(request, str(redirect_uri))

@router.route('/signup')
async def signup(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


@router.get('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        logger.info('OAuthError', e)
        return RedirectResponse(url='/')
    request.session['user'] = access_token['userinfo']
    user_email = access_token['userinfo'].get('email')

    # if email is not registered, register new user
    registered = get_user_by_email(db=db, email=user_email)
    logger.info('reg', registered)
    if not registered:
        user = {'email': user_email, "password": None, "google_auth": True}
        create_user(db=db, user=UserCreate(**user))

    return RedirectResponse(url='/')

@router.get('/')
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<a href=/login>Login</a>')
        # return {"loggedIn": True, "name": name}
    # return {"loggedIn": False, "name": None}


@router.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
