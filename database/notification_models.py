from database import db
from sqlalchemy import func
from enum import Enum


class EthNotificationTypes(Enum):
    APN = 1  # Apple notification
    FCM = 2  # Firebase cloud messaging


class EthNotificationEndpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eth_address = db.Column(db.String(255), index=True)
    device_token = db.Column(db.String(255), index=True)
    type = db.Column(db.Enum(EthNotificationTypes))
    active = db.Column(db.Boolean())
    verified = db.Column(db.Boolean())
    created_at = db.Column(
        db.DateTime(
            timezone=True),
        server_default=func.now())
    expires_at = db.Column(db.DateTime(timezone=True))
