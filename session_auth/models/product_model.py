from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from session_auth.core.configs import settings


class ProductModel(settings.DBBaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    url = Column(String(256))
    description = Column(String(256))
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("UserModel", back_populates="products", lazy="joined")
