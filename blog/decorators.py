from graphql_jwt import exceptions


def verification_required(fn):
    def wrapper(root, info, **kwargs):
        user = info.context.user
        try:
            if not user.status.verified:
                raise exceptions.PermissionDenied()
        except:
            raise exceptions.PermissionDenied()
        finally:
            return fn(root, info, **kwargs)

    return wrapper
