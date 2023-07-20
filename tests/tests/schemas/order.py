import jsonschema


class OrderSchema:
    input_schema = {
        'type': 'object',
        'properties': {
            'stock_symbol': {
                'type': 'string',
            },
            'quantity': {
                'type': 'number',
            },
        },
        'required': ['stock_symbol', 'quantity']
    }

    output_schema = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'string',
            },
            'stock_symbol': {
                'type': 'string',
            },
            'quantity': {
                'type': 'number',
            },
            'status': {
                'type': 'string',
                'enum': ['PENDING', 'EXECUTED', 'CANCELLED']
            },
        },
        'required': ['id', 'stock_symbol', 'quantity', 'status']
    }

    list_output_schema = {
        'type': 'object',
        'properties': {
            'orders': {
                'type': 'array',
                "items": output_schema
            }
        },
        'required': ['orders']
    }

    @classmethod
    def validate_input(cls, data):
        jsonschema.validate(instance=data, schema=cls.input_schema)

    @classmethod
    def validate_output(cls, data):
        jsonschema.validate(instance=data, schema=cls.output_schema)

    @classmethod
    def validate_list_output(cls, data):
        jsonschema.validate(instance=data, schema=cls.list_output_schema)
