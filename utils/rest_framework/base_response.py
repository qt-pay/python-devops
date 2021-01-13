from rest_framework.response import Response
from collections import OrderedDict
def new_response(code=2000, data='successful',message='successful', **kwargs):
    result = OrderedDict([
        ('code', code),
        ('message', message),
        ('data', data),
    ])
    result.update(**kwargs)
    return Response(result)