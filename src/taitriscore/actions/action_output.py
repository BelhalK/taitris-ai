from typing import Dict, Type

from pydantic import BaseModel, create_model, field_validator, model_validator


class ActionOutput:
    content: str
    instruct_content: BaseModel

    def __init__(self, content: str, instruct_content: BaseModel):
        self.content = content
        self.instruct_content = instruct_content

    @classmethod
    def create_model_class(cls, class_name: str, mapping: Dict[str, Type]):
        new_class = create_model(class_name, **mapping)

        @field_validator("*", allow_reuse=True)
        def check_name(cls, v, info):
            if info.field_name not in mapping.keys():
                raise ValueError(f"Unrecognized block: {info.field_name}")
            return v

        @model_validator(mode="before")
        def check_missing_fields(cls, values):
            required_fields = set(mapping.keys())
            missing_fields = required_fields - set(values.keys())
            if missing_fields:
                raise ValueError(f"Missing fields: {missing_fields}")
            return values

        new_class.__validator_check_name = classmethod(check_name)
        new_class.__model_validator_check_missing_fields = classmethod(
            check_missing_fields
        )
        return new_class
