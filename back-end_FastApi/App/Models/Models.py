from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text, BigInteger, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.types import Text

from App.output_ports.db.Connexion import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    email_verified_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    password = Column(String(255), nullable=False)
    remember_token = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=True)
    adress = Column(String(255), nullable=True)
    phone = Column(Integer, nullable=True)
    