from pydantic import BeforeValidator
from typing import Annotated
from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` in the API so that it can be easily serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]
