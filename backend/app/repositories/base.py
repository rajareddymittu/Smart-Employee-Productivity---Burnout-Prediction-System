from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def create(self, obj_in: Dict[str, Any]) -> T:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def get(self, id: int) -> Optional[T]:
        """Get a record by ID."""
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination."""
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def get_by_filter(self, **filters) -> Optional[T]:
        """Get a single record by filters."""
        query = self.session.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first()

    def get_all_by_filter(self, skip: int = 0, limit: int = 100, **filters) -> List[T]:
        """Get all records by filters with pagination."""
        query = self.session.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.offset(skip).limit(limit).all()

    def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[T]:
        """Update a record."""
        db_obj = self.get(id)
        if db_obj:
            for key, value in obj_in.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)
            self.session.commit()
            self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Delete a record."""
        db_obj = self.get(id)
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
            return True
        return False

    def count(self, **filters) -> int:
        """Count records by filters."""
        query = self.session.query(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.count()
