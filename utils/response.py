from rest_framework.response import Response


def ResponseSucess(data=None, *args, **kwargs):
    return Response(
        data={'success': True, 'data': data},
        headers={'Access-Control-Allow-Origin': '*'},
        *args, **kwargs
    )


def ResponseError(error=None, *args, **kwargs):
    return Response(
        data={'success': False, 'message': error},
        headers={'Access-Control-Allow-Origin': '*'},
        *args, **kwargs
    )
