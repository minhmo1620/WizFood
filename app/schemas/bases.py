from marshmallow import Schema, pre_load


class Base(Schema):
    @pre_load
    def strip_data(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data