"""
Base CRUD operations with type safety.

This module provides a generic base class for CRUD operations that can be
inherited by specific CRUD classes for different models.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session

from app.db.models.base import BaseModel as DBBaseModel

# Type variables for generic CRUD operations
ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD class with default methods for Create, Read, Update, Delete.

    This class provides basic CRUD operations that can be extended by
    specific CRUD classes for different models.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with model class.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.

        Args:
            db: Database session
            id: Record ID

        Returns:
            Model instance or None if not found
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination and filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Field name to order by
            order_desc: Whether to order in descending order
            filters: Dictionary of field filters

        Returns:
            List of model instances
        """
        query = db.query(self.model)

        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        # IN filter for lists
                        query = query.filter(getattr(self.model, field).in_(value))
                    else:
                        # Equality filter
                        query = query.filter(getattr(self.model, field) == value)

        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            if order_desc:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            db: Database session
            obj_in: Pydantic schema with data to create

        Returns:
            Created model instance
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing record.

        Args:
            db: Database session
            db_obj: Existing model instance
            obj_in: Pydantic schema or dictionary with update data

        Returns:
            Updated model instance
        """
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        Delete a record by ID.

        Args:
            db: Database session
            id: Record ID to delete

        Returns:
            Deleted model instance or None if not found
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    # Additional useful methods

    def get_by_field(
        self,
        db: Session,
        field_name: str,
        field_value: Any
    ) -> Optional[ModelType]:
        """
        Get a record by any field value.

        Args:
            db: Database session
            field_name: Name of the field to filter by
            field_value: Value to match

        Returns:
            Model instance or None if not found
        """
        if not hasattr(self.model, field_name):
            return None

        return db.query(self.model).filter(
            getattr(self.model, field_name) == field_value
        ).first()

    def get_multi_by_field(
        self,
        db: Session,
        field_name: str,
        field_values: List[Any]
    ) -> List[ModelType]:
        """
        Get multiple records by field values.

        Args:
            db: Database session
            field_name: Name of the field to filter by
            field_values: List of values to match

        Returns:
            List of model instances
        """
        if not hasattr(self.model, field_name):
            return []

        return db.query(self.model).filter(
            getattr(self.model, field_name).in_(field_values)
        ).all()

    def exists(self, db: Session, id: Any) -> bool:
        """
        Check if a record exists by ID.

        Args:
            db: Database session
            id: Record ID

        Returns:
            True if record exists, False otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first() is not None

    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filters.

        Args:
            db: Database session
            filters: Optional dictionary of field filters

        Returns:
            Number of records
        """
        query = db.query(self.model)

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)

        return query.count()

    def search(
        self,
        db: Session,
        *,
        search_term: str,
        search_fields: List[str],
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Search records by text in specified fields.

        Args:
            db: Database session
            search_term: Text to search for
            search_fields: List of field names to search in
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching model instances
        """
        if not search_term or not search_fields:
            return []

        # Build search conditions
        conditions = []
        for field_name in search_fields:
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                conditions.append(field.ilike(f"%{search_term}%"))

        if not conditions:
            return []

        return db.query(self.model).filter(
            or_(*conditions)
        ).offset(skip).limit(limit).all()

    def bulk_create(self, db: Session, *, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        """
        Create multiple records in bulk.

        Args:
            db: Database session
            objs_in: List of Pydantic schemas with data to create

        Returns:
            List of created model instances
        """
        db_objs = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db_objs.append(db_obj)

        db.add_all(db_objs)
        db.commit()

        for db_obj in db_objs:
            db.refresh(db_obj)

        return db_objs

    def bulk_update(
        self,
        db: Session,
        *,
        updates: List[Dict[str, Any]]
    ) -> List[ModelType]:
        """
        Update multiple records in bulk.

        Args:
            db: Database session
            updates: List of dictionaries with 'id' and update fields

        Returns:
            List of updated model instances
        """
        updated_objs = []

        for update_data in updates:
            if 'id' not in update_data:
                continue

            obj_id = update_data.pop('id')
            db_obj = self.get(db, obj_id)

            if db_obj:
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                updated_objs.append(db_obj)

        if updated_objs:
            db.commit()
            for db_obj in updated_objs:
                db.refresh(db_obj)

        return updated_objs

    def bulk_delete(self, db: Session, *, ids: List[int]) -> int:
        """
        Delete multiple records by IDs.

        Args:
            db: Database session
            ids: List of record IDs to delete

        Returns:
            Number of deleted records
        """
        deleted_count = db.query(self.model).filter(
            self.model.id.in_(ids)
        ).delete(synchronize_session=False)

        db.commit()
        return deleted_count
