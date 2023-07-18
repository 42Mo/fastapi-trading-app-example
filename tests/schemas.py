order_input_schema = {
    'type': 'object',
    'properties': {
        'stoks': {
            'type': 'string',
        },
        'quantity': {
            'type': 'number',
        },
    },
    'required': ['stoks', 'quantity']
}

order_output_schema = {
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

orders_output_schema = {
    'type': 'object',
    'properties': {
        'orders': {
            'type': 'array',
            "items": {
                "type": "object",
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
        }
    },
    'required': ['orders']
}

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