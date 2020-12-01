from bbcsocial import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    joined = db.Column(db.DateTime, nullable=False, default=datetime.now)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.now)
    last_message_read_time = db.Column(db.DateTime, default=datetime.now)

    def unread_message_count(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        msgcounts=Message.query.filter_by(recipient_id=self.id, is_seen=False).count()
        return msgcounts

    def __repr__(self):
        return f"User{self.id}: [{self.fullname}, {self.username}, {self.email}, {self.image_file}]"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140), index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    is_seen = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Message{self.id}: [ {self.message} (Sent by User{self.sender_id} & received by User{self.recipient_id}) ]"


