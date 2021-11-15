from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework import status


def get_error_msg(data, key):
    if isinstance(data, str):
        return f"{key}: {data.lower()}"
    elif isinstance(data, dict):
        key = list(data.keys())[0]
        data = data[key]
        if isinstance(data, list):
            return f"{key}: {data[0].lower()}"
        elif isinstance(data, str):
            return f"{key}: {data.lower()}"
    return get_error_msg(data, key)


def custom_exception_handler(exc, context):

    handlers = {
        'ParseError': _handle_generic_error,
        'AuthenticationFailed': _handle_generic_error,
        'NotAuthenticated': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotFound': _handle_generic_error,
        'MethodNotAllowed': _handle_generic_error,
        'NotAcceptable': _handle_generic_error,
        'UnsupportedMediaType': _handle_generic_error,
        'Throttled': _handle_generic_error,
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
    }

    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    data = {'data': {}, 'status': False}

    if response is not None:
        if response.status_code == 400:
            key = list(response.data.keys())[0]
            value = response.data[key]
            data['message'] = get_error_msg(value, key)
            response.data = data
        elif response.data['detail']:
            data['message'] = response.data['detail']
            response.data = data
    return response


def _handle_generic_error(exc, context, response):

    data = {'data': {}, 'status': False}

    if response is not None:
        key = list(response.data.keys())[0]
        value = response.data[key]
        data['message'] = get_error_msg(value, key)
        response.data = data
    elif response.data['detail']:
        data['message'] = response.data['detail']
        response.data = data
    return response


def server_error(request, *args, **kwargs):
    """
    Generic 500 error handler.
    """
    data = {
        'error': 'Server Error (500)'
    }
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def bad_request(request, exception, *args, **kwargs):
    """
    Generic 400 error handler.
    """
    data = {
        'error': 'Bad Request (400)'
    }
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)