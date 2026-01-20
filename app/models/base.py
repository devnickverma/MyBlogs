from app.core.database import Base
# This file can be used for common mixins later (IDMixin, TimestampMixin)
# For now, we import Base here to allow 'app.models.base.Base' usage if preferred,
# but usually we import Base from core.database or define it here.
# To avoid circular imports, let's keep Base in core/database.py and just re-export or leave empty.
# Actually, let's make this file useful by adding a TimestampMixin.

from sqlalchemy import Column, DateTime, func

class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
