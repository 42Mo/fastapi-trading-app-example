import json

import allure
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
    @allure.step("Validate error schema")
    def validate_error(cls, data):
        jsonschema.validate(instance=data, schema=cls.error_schema)
        allure.attach(
            json.dumps(cls.error_schema, indent=2),
            name="Reference Schema",
            attachment_type=allure.attachment_type.JSON
        )
