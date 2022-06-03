from typing import Any
from pydantic import BaseModel, create_model

Models = set()

def model(cls):
    def register_model():
        Models.add(cls)
        return cls

    return register_model

class Field:
    __slots__ = ['pydobj', 'primary', 'private', 'Insertable', 'Updatable', 'Deletable', 'alias', 'ref', 'sub']
    def __init__(self, pydobj, primary=False, private=False, Insertable=True, Updatable=True, Deletable=True, alias=None, ref=None, sub=None):
        self.pydobj = pydobj
        self.primary = primary
        self.private = private
        self.Insertable = Insertable
        self.Updatable = Updatable
        self.Deletable = Deletable
        self.alias = alias
        self.ref = ref
        self.sub = sub

    @staticmethod
    def by_name(fields: list, name: str) -> "Field":
        return filter(lambda field: field.name == name, fields)

    @staticmethod
    def aliased(fields: list) -> dict[str, "Field"]:
        return {(field.alias or field.name): field for field in fields}

    @staticmethod
    def filtered_by(fields: list, feature: str, value: Any=True, aliased: bool=False) -> dict[str, "Field"]:
        if aliased:
            return {(field.alias or field.name): field for field in fields if getattr(field, feature) == value}
        else:
            return {field.name: field for field in fields if getattr(field, feature) == value}

class FarmBuilder:
    __slots__ = ['all_fields', 'farm_fields', 'public_fields', 'private_fields', 'ref_fields', 'sub_fields']
    properties = ['Insertable', 'Updatable', 'Deletable']

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
        self.public_fields = filter(lambda field: field.private == False, self.all_fields)
        self.private_fields = filter(lambda field: field.private == True, self.all_fields)
        self.ref_fields = filter(lambda field: field.ref is not False, self.all_fields)
        self.sub_fields = filter(lambda field: field.sub is not False, self.all_fields)

        for property in FarmBuilder.properties:
            self.farm_fields[property] = Field.filtered_by(self.all_fields, property, aliased=True)
            
        farms = {}
        for property in FarmBuilder.properties:
            farm_name = f'{model_name}{property}'
            farms[property] = self.build_farm(farm_name, property)

        return farms
        
    def build_farm(self, farm_name: str, property_name: str, **margs) -> BaseModel:
        if not property_name in FarmBuilder.properties:
            return
        
        farm_fields = self.farm_fields[property_name]
        model_fields = {field_name: field.pydobj for field_name, field in farm_fields.items()}
        
        return create_model(farm_name, **model_fields, **margs)
