from datetime import datetime

from flask import Blueprint, abort, redirect, render_template, session, url_for
from flask_login import current_user, login_required
from flask_socketio import emit, join_room, leave_room
from hamrokurakani import db, socketio
from hamrokurakani.core.des import DesKey
from hamrokurakani.models import Message, User

chyat = Blueprint('chat', __name__, template_folder='templates')


@chyat.route('/')
@login_required
def home():
    users = User.query.all()
    total_users = len(list(users))
    return render_template('chat/users.html', users=users, total_users=total_users)


@chyat.route('/chatwith/<string:user>')
@login_required
def chatwith(user):
    getuser = User.query.filter_by(username=user).first_or_404()
    messages = []
    session['receiver_id'] = getuser.id
    session['room'] = int(getuser.id) * int(current_user.id)
    msgs_received = list(Message.query.filter_by(
        recipient_id=current_user.id, sender_id=getuser.id).all())
    msgs_sent = list(Message.query.filter_by(
        recipient_id=getuser.id, sender_id=current_user.id).all())
    messages = msgs_received + msgs_sent
    messages.sort(key=lambda order_by: order_by.timestamp)
    current_user.last_message_read_time = datetime.now()
    for message in msgs_received:
        message.is_seen = True
    db.session.commit()
    return render_template('chat/chatter.html', getuser=getuser, users=User.query.all(), messages=messages)


@chyat.route("/chatwith/<string:user>/deletemessage/<int:id>/")
@login_required
def deletemessage(user, id):
    message = Message.query.filter_by(id=id).first_or_404()
    if not current_user.is_authenticated and message.author != current_user:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('chat.chatwith', user=user))


##? SOCKET WORK BELOW ################################################################


@socketio.on('joined', namespace='/chatwith')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': 'You entered the room.'}, room=room)


@socketio.on('text', namespace='/chatwith')
def text(message):
    key = "kisan123".encode()
    manager = DesKey(key)
    profileimg = f"/static/profilepics/{current_user.image_file}"
    receiver = session.get('receiver_id')
    room = session.get('room')
    the_msg = manager.encrypt(message["msg"].encode(), padding=True)
    user = User.query.filter_by(id=receiver).first_or_404()
    msg = Message(author=current_user, recipient=user,
                  message=the_msg)
    db.session.add(msg)
    user.unread_message_count()
    db.session.commit()
    emit('message', {
         'msg': message['msg'], 'userImg': profileimg}, room=room, include_self=False)


@socketio.on('left', namespace='/chatwith')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', room=room)
