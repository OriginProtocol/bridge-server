from database import db
from datetime import datetime
from enum import Enum


class AttestationTypes(Enum):
    PHONE = 1
    EMAIL = 2
    AIRBNB = 3
    FACEBOOK = 4
    TWITTER = 5


class Attestation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.Enum(AttestationTypes))
    eth_address = db.Column(db.String)
    value = db.Column(db.String)
    signature = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime(timezone=True))
