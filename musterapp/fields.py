from django.core.exceptions import ValidationError
from django.forms import fields
from django.db import models

class BBoxFormField(fields.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        return BBoxField.get_prep_value(value)

    def clean(self, value):
        return BBoxField.parse_bbox(value)


class BBoxField(models.CharField):
    description = "A bounding box for polygons (minx, miny, maxx, maxy)"

    _dict_keys = ("x", "y", "width", "height")

    def __init__(self, *args, **kwargs):
        # 4 Times maxint 64 in base10 and 3 spaces
        kwargs['max_length'] = 79
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    @staticmethod
    def parse_bbox(value):
        if value is None:
            return value

        if not value:
            return None

        if isinstance(value, dict):
            if sorted(value.keys()) != sorted(BBoxField._dict_keys):
                raise ValidationError("Invalid BBox")
            return value

        if isinstance(value, str):
            value = value.split(" ")

        if len(value) is not 4:
            raise ValidationError("Invalid value for BBox")

        bbox = dict(zip(BBoxField._dict_keys, map(int, value)))
        return bbox

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.parse_bbox(value)

    def to_python(self, value):
        return self.parse_bbox(value)

    @staticmethod
    def get_prep_value(value):
        if value is None:
            return ""

        if isinstance(value, dict):
            if sorted(value.keys()) != sorted(BBoxField._dict_keys):
                raise ValidationError("Invalid BBox")
            value = (value["x"], value["y"], value["width"], value["height"])

        if len(value) is not 4:
            raise ValidationError("Invalid value for BBox")

        value = " ".join(map(str, value))
        return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        return '' if val is None else self.get_prep_value(val)

    def formfield(self, **kwargs):
        defaults = {"help_text": "Enter BBox in format 'x y width height'",
                    "form_class": BBoxFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
