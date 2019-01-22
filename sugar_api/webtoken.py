import jwt
from sanic import Blueprint
from sanic.response import json

from sugar_odm import Model

from sugar_api import Error


class WebToken(object):

    __content_type__ = 'application/vnd.api+json'

    @classmethod
    async def payload(cls, username, password):
        raise NotImplementedError('WebToken.payload not implemented.')

    @classmethod
    def blueprint(cls, *args, **kargs):

        cls.secret = kargs.get('secret')

        if not cls.secret:
            raise Exception('Secret not provided.')

        if 'secret' in kargs:
            del kargs['secret']

        cls.url = kargs.get('url', 'authorization')

        if 'url' in kargs:
            del kargs['url']

        cls.token_algorithm = kargs.get('token_algorithm', 'HS256')

        if 'token_algorithm' in kargs:
            del kargs['token_algorithm']

        if not len(args) > 0:
            args = [ cls.url ]

        bp = Blueprint(*args, **kargs)

        @bp.post(cls.url)
        @cls._content_type
        @cls._accept
        async def post(*args, **kargs):
            return await cls._post(*args, **kargs)

        return bp

    @classmethod
    def _content_type(cls, handler):
        async def decorator(request, *args, **kargs):
            content_type = request.headers.get('Content-Type')
            if not content_type or not content_type == cls.__content_type__:
                error = Error(
                    title = 'Invalid Content-Type Header',
                    detail = 'The Content-Type header provided is of an invalid type.',
                    status = 415
                )
                return json({ 'errors': [ error.serialize() ] }, status=415)
            return await handler(request, *args, **kargs)
        return decorator

    @classmethod
    def _accept(cls, handler):
        async def decorator(request, *args, **kargs):
            accept = request.headers.get('Accept')
            if not accept or not accept == cls.__content_type__:
                error = Error(
                    title = 'Invalid Accept Header',
                    detail = 'The Accept header provided is of an invalid type.',
                    status = 415
                )
                return json({ 'errors': [ error.serialize() ] }, status=415)
            return await handler(request, *args, **kargs)
        return decorator

    @classmethod
    async def _post(cls, request):

        data = None

        if request.json:

            data = request.json.get('data')

        if not data:

            error = Error(
                title = 'Create Token Error',
                detail = 'No data provided.',
                status = 403
            )

            return json({ 'errors': [ error.serialize() ] }, status=403)

        if not isinstance(data, dict):

            error = Error(
                title = 'Create Token Error',
                detail = 'Data is not a JSON object.',
                status = 403
            )

            return json({ 'errors': [ error.serialize() ] }, status=403)

        username = data.get('username')

        if not username:

            message = 'Missing username.'.format(
                username = username
            )

            error = Error(
                title = 'Create Token Error',
                detail = message,
                status = 403
            )

            return json({ 'errors': [ error.serialize() ] }, status=403)

        password = data.get('password')

        if not password:

            message = 'Missing password.'.format(
                password = password
            )

            error = Error(
                title = 'Create Token Error',
                detail = message,
                status = 403
            )

            return json({ 'errors': [ error.serialize() ] }, status=403)

        try:

            payload = await cls.payload(username, password)

        except Exception as e:

            error = Error(
                title = 'Create Token Error',
                detail = str(e),
                status = 403
            )

            return json({ 'errors': [ error.serialize() ] }, status=403)

        token = jwt.encode(payload, cls.secret, algorithm=cls.token_algorithm)

        return json({ 'data': { 'token': token } }, 200)
