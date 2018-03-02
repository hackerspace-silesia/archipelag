from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = 400
    return response


def get_proper_format_for_valid_exception(error):
    try:
        details = error.detail
    except ValueError:
        return error
    else:
        if isinstance(details, list):
            error = error.detail[0]
        else:
            error = error.detail
        return error