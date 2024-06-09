from typing import Dict, Type

from pydantic import BaseModel, create_model, field_validator, model_validator


class ActionOutput:
    """Class representing an action output with content and instructional content."""
    content: str
    instruct_content: BaseModel

    def __init__(self, content: str, instruct_content: BaseModel):
        """
        Initialize ActionOutput with content and instruct_content.

        Args:
            content (str): The content as a string.
            instruct_content (BaseModel): The instructional content as a Pydantic BaseModel.
        """
        self.content = content
        self.instruct_content = instruct_content

    @classmethod
    def create_model_class(cls, class_name: str, mapping: Dict[str, Type[BaseModel]]) -> Type[BaseModel]:
        """
        Dynamically create a Pydantic model class with field validators.

        Args:
            class_name (str): The name of the new class.
            mapping (Dict[str, Type[BaseModel]]): A dictionary mapping field names to their types.

        Returns:
            Type[BaseModel]: The newly created Pydantic model class.
        """
        # Create a new Pydantic model class with the given name and field mappings
        new_class = create_model(class_name, **mapping)

        # Validator to check if the field name exists in the provided mapping
        @field_validator("*", allow_reuse=True)
        def check_name(cls, v, info):
            if info.field_name not in mapping:
                raise ValueError(f"Unrecognized block: {info.field_name}")
            return v

        # Validator to check for missing fields before model instantiation
        @model_validator(mode="before")
        def check_missing_fields(cls, values):
            required_fields = set(mapping.keys())
            missing_fields = required_fields - set(values.keys())
            if missing_fields:
                raise ValueError(f"Missing fields: {missing_fields}")
            return values

        # Add the validators to the new class
        new_class.__validator_check_name = classmethod(check_name)
        new_class.__model_validator_check_missing_fields = classmethod(check_missing_fields)

        return new_class