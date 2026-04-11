from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import date
from .text2sql_base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    order_date = Column(Date, default=date.today)
    status = Column(String, nullable=False)
    total_amount = Column(Integer, nullable=False)