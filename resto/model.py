from typing import Any, TypeVar
from pydantic import BaseModel, create_model
from resto.util import BaseUtil

Models = set()
Model = TypeVar('Model')


def model():
    def register_model(cls):
        Models.add(cls)
        return cls

    return register_model


class Field:
    __slots__ = [
        'name',
        'pydobj',
        'primary',
        'private',
        'Insertable',
        'Updatable',
        'Filterable',
        'alias',
        'ref',
        'sub',
    ]

    def __init__(
        self,
        pydobj,
        name=None,
        primary=False,
        private=False,
        Insertable=True,
        Updatable=True,
        Filterable=True,
        alias=None,
        ref=None,
        sub=None,
    ):
        self.name = name
        self.pydobj = pydobj
        self.primary = primary
        self.private = private
        self.Insertable = Insertable
        self.Updatable = Updatable
        self.Filterable = Filterable
        self.alias = alias
        self.ref = ref
        self.sub = sub

    def get(self, slot, default_val=None):
        val = getattr(self, slot)
        if not val:
            return default_val
        return val

    @staticmethod
    def by_name(fields: list, name: str) -> "Field":
        return filter(lambda field: field.name == name, fields)

    @staticmethod
    def aliased(fields: list) -> dict[str, "Field"]:
        return {(field.alias or field.name): field for field in fields}

    @property
    def pydobj_normalized(self):
        if isinstance(self.pydobj, tuple) and self.pydobj[1] == ...:
            return (self.pydobj[0], None)
        return self.pydobj

    @staticmethod
    def filtered_by(
        fields: list, feature: str, value: Any = True, aliased: bool = False
    ) -> dict[str, "Field"]:
        if aliased:
            return {
                (field.alias or field.name): field
                for field in fields
                if getattr(field, feature) == value
            }
        else:
            return {
                field.name: field
                for field in fields
                if getattr(field, feature) == value
            }


class FarmBuilder:
    __slots__ = [
        'all_fields',
        'farm_fields',
        'public_fields',
        'private_fields',
        'ref_fields',
        'sub_fields',
    ]

    properties = {
        'Insertable': {'normalize': False},
        'Updatable': {'normalize': False},
        'Filterable': {'normalize': True},
    }

    def __init__(self):
        self.all_fields = {}
        self.farm_fields = {}
        for property in FarmBuilder.properties:
            self.farm_fields[property] = {}

    def seed_field(self, field: Field):
        self.all_fields[field.name] = field

    def seed_fields(self, fields: list[Field]):
        valid_fields = filter(lambda field: isinstance(field, Field), fields)

        for field in valid_fields:
            self.seed_field(field)

    def build_farms(self, model_name):
        self.public_fields = Field.filtered_by(
            self.all_fields.values(), 'private', value=False
        )
        self.private_fields = Field.filtered_by(
            self.all_fields.values(), 'private', value=True
        )
        self.ref_fields = Field.filtered_by(self.all_fields.values(), 'ref', value=True)
        self.sub_fields = Field.filtered_by(self.all_fields.values(), 'sub', value=True)

        for property in FarmBuilder.properties:
            self.farm_fields[property] = Field.filtered_by(
                self.all_fields.values(),
                property,
                aliased=True,
            )

        farms = {}
        for property in FarmBuilder.properties:
            farm_name = f'{model_name}{property}'
            farms[property] = self.build_farm(farm_name, property)

        return farms

    def build_farm(self, farm_name: str, property_name: str, **model_kwargs) -> BaseModel:
        if not property_name in FarmBuilder.properties:
            return

        farm_fields = self.farm_fields[property_name]
        field_attr = (
            'pydobj_normalized'
            if FarmBuilder.properties[property_name]['normalize']
            else 'pydobj'
        )

        model_fields = {
            field_name: field.get(field_attr)
            for field_name, field in farm_fields.items()
        }

        model = create_model(farm_name, **model_fields, **model_kwargs)
        return model

    def load_fields(self, schema):
        for fieldname, field in schema.items():
            if not isinstance(field, Field):
                field = Field(field, name=fieldname)
            else:
                field.name = fieldname

            self.seed_field(field)


    @staticmethod
    def build_lonely_farm(name: str, fields: dict[str, Any], **model_kwargs):
        model = create_model(name, **fields, **model_kwargs)
        return model