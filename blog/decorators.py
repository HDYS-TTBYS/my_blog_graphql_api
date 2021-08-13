from graphql_jwt import exceptions
from functools import wraps


def verification_required(fn):
    @wraps(fn)
    def wrapper(root, info, **input):
        try:
            if not info.context.user.status.verified:
                raise exceptions.PermissionDenied()
        except:
            raise exceptions.PermissionDenied()

        return fn(root, info, **input)

    return wrapper
