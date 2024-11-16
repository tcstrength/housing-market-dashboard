from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column, Integer, String
from hmd.entity.base_entity import BaseEntity

class PendingPostEntity(BaseEntity):
    __tablename__ = "pending_post"
    __table_args__ = {'extend_existing': True}
    post_id = Column(Integer, primary_key=True, autoincrement=False)
    post_url = Column(String(1024))
    post_type = Column(String(16))
    status = Column(String(1))

    # Method to convert SQLAlchemy model instance to a dictionary
    def to_dict(self):
        return {
            "post_id": self.post_id,
            "post_url": self.post_url,
            "post_type": self.post_type,
            "status": self.status,
        }

    # Static method to create model instance from dictionary
    @staticmethod
    def from_dict(data):
        return PendingPostEntity(
            post_id=data.get("post_id"),
            post_url=data.get("post_url"),
            post_type=data.get("post_type"),
            status=data.get("status"),
        )