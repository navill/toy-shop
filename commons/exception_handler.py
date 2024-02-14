from django.http import Http404

from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

VALIDATION_CODE = 999
UNKNOWN_CODE = 9999


def handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_detail = exc.args[0] if isinstance(exc, Http404) else exc.default_detail
        data = {'error_code': getattr(exc, 'error_code', None),
                'error_detail': error_detail,
                'error_class': exc.__class__.__name__}

        if isinstance(exc, serializers.ValidationError):
            data = _validation_error_handler(response, data)

        elif isinstance(exc, Http404):
            data['error_code'] = 'not_found'

        else:
            error_detail = response.data.pop('detail', None)
            error_code = error_detail.code if isinstance(error_detail, ErrorDetail) else UNKNOWN_CODE
            targets = {'msg': str(error_detail), 'code': error_code} if error_detail is not None else 'N/A'
            data['targets'] = [targets]

        response.data = data
    return response


def _validation_error_handler(response, data) -> dict:
    data['error_code'] = VALIDATION_CODE
    targets = list()

    if isinstance(response.data, list):
        if isinstance(response.data[-1], dict):
            try:
                targets = [[{'msg': f"{key}: {val[0]}", 'code': val[0].code} for key, val in data.items()][0] for data
                           in response.data]
            except IndexError:
                targets = [
                    [{'msg': field_name, 'code': list_val[0]}
                     for field_name, list_val in dict_data.items()][0]
                    for dict_data in response.data if dict_data
                ]
        else:
            targets = [{'msg': str(error_detail), 'code': error_detail.code} for error_detail in
                       response.data]
    elif isinstance(response.data, dict):
        targets = [{'msg': f"{key}: {val[0]}", 'code': val[0].code} for key, val in response.data.items()]

    data['targets'] = targets
    return data
