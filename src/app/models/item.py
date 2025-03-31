from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    """
    Base model for Item attributes shared across create/update/read.
    """
    name: str = Field(..., description="The name of the item")
    description: Optional[str] = Field(None, description="An optional description of the item")

class ItemCreate(ItemBase):
    """
    Model used when creating an item (e.g., in a POST request).
    May include additional fields specific to creation.
    """
    pass # No additional fields for creation in this example

class ItemUpdate(ItemBase):
    """
    Model used when updating an item (e.g., in a PUT/PATCH request).
    All fields are optional for partial updates.
    """
    name: Optional[str] = None
    description: Optional[str] = None

class ItemInDBBase(ItemBase):
    """
    Base model for items as stored in the database.
    Includes database-specific fields like _id and _rev for CouchDB.
    """
    id: str = Field(..., alias="_id", description="Document ID in CouchDB")
    rev: Optional[str] = Field(None, alias="_rev", description="Document revision in CouchDB")

    class Config:
        populate_by_name = True # Allows using alias names (_id, _rev)

class Item(ItemInDBBase):
    """
    Model representing an item retrieved from the database (e.g., in a GET response).
    Inherits all fields from ItemInDBBase.
    """
    pass # No additional fields for response in this example

# Example Usage:
# item_data = {"name": "My Item", "description": "A cool item"}
# new_item = ItemCreate(**item_data)
# db_item_data = {"_id": "doc123", "_rev": "1-abc", "name": "DB Item", "description": "From DB"}
# db_item = Item(**db_item_data)
