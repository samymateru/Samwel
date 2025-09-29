from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class UserNotificationColumns(str, Enum):
    ID = "id"
    USER = "user_id"
    TITLE = "title"
    MESSAGE = "message"
    STATUS = "status"
    READ_AT = "read_at"
    CREATED_AT = "created_at"


class NotificationsStatus(str, Enum):
    NEW = "New"
    OPENED = "Opened"
    ARCHIVED = "Archived"


class ReadUserNotification(BaseModel):
    id: str
    user_id: str
    title: Optional[str] = None
    message: str
    status: NotificationsStatus
    read_at: Optional[datetime] = None
    created_at: datetime

class CreateNotifications(BaseModel):
    id: str
    user_id: str
    title: Optional[str] = None
    message: str
    status: NotificationsStatus
    read_at: Optional[datetime] = None
    created_at: datetime


class UpdateNotificationRead(BaseModel):
    status: NotificationsStatus
    read_at: datetime