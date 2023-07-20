import jsonschema


class ErrorSchema:
    error_schema = {
        'type': 'object',
        'properties': {
            'code': {
                'type': 'integer',
            },
            'message': {
                'type': 'string',
            },
        },
        'required': ['code', 'message']
    }

    @classmethod
    def validate_error(cls, data):
        jsonschema.validate(instance=data, schema=cls.error_schema)
