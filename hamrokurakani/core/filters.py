from datetime import datetime
from flask import url_for, current_app, Blueprint
from hamrokurakani.models import Message
from flask_login import current_user
from hamrokurakani.core.des import manager

core = Blueprint('core', __name__)


@core.app_template_filter('humanify')
def human_date(datetime_of_event):

    currenttime = datetime.now()
    curryear, currmnth, currday = currenttime.year, currenttime.month, currenttime.day
    currhour, currmin, currsec = currenttime.hour, currenttime.minute, currenttime.second
    now = datetime(curryear, currmnth, currday, currhour, currmin, currsec)
    eventhappening = datetime_of_event
    posyear = eventhappening.year
    posmnth = eventhappening.month
    posday = eventhappening.day
    poshour = eventhappening.hour
    posmin = eventhappening.minute
    possec = eventhappening.second

    post = datetime(posyear, posmnth, posday, poshour, posmin, possec)

    #post = datetime(2019, 1, 1, 13, 40, 20)
    diff = abs(now-post)
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff <= 0:

        if second_diff < 60:
            if second_diff < 10:
                return "just now"

            message = str(int(second_diff)) + " seconds"
            return message

        if second_diff < 3600:
            m = int(second_diff / 60)
            if m == 1:
                return "1 minute"
            message = str(m) + " minutes"
            return message

        if second_diff < 86400:
            h = int(second_diff / 3600)
            if h == 1:
                return "1 hour"
            message = str(h) + " hours"
            return message

    if day_diff < 7:
        if day_diff == 1:
            return "1 day"
        message = str(day_diff) + " days"
        return message

    if day_diff < 31:
        w = int(day_diff / 7)
        if w == 1:
            return "1 week"
        message = str(w) + " weeks"
        return message

    if day_diff < 365:
        mnth = int(day_diff / 30)
        if mnth == 1:
            return "1 month"
        message = str(mnth) + " months"
        return message

    y = int(day_diff / 365)
    if y == 1:
        return "1 year"
    message = str(y) + " years"
    return message

@core.app_template_filter('decrypt')
def decrypt_message(given_message):
    return manager(given_message,"kisan123","decrypt")


@core.app_template_filter('isactive')
def is_active(lastmessagereadtime):

    currenttime = datetime.now()
    lastread = lastmessagereadtime
    diff = abs(currenttime-lastread)
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff <= 0 and second_diff < 60:
        message = "active now"
        return message

    elif day_diff <= 0 and second_diff < 3600:
        m = int(second_diff / 60)
        if m == 1:
            message = "active 1m ago"
            return message

        elif m <= 10:
            message = "active " + str(m) + "m ago"
            return message

        else:
            message = "offline"
            return message

    else:
        message = "offline"
        return message


@core.app_template_filter('differencebetwn')
def difference_between(firstdate, seconddate):

    diff = abs(firstdate-seconddate)
    second_diff = diff.seconds
    m = int(second_diff / 60)
    if m <= 3:
        return True
    else:
        return False


@core.app_template_filter('lastmessage')
def last_message(sender):
    msg_received = Message.query.filter_by(
        recipient_id=current_user.id, sender_id=sender.id).order_by(Message.timestamp.desc()).first()
    msg_sent = Message.query.filter_by(
        sender_id=current_user.id, recipient_id=sender.id).order_by(Message.timestamp.desc()).first()
    if msg_received and not msg_sent:
        return msg_received.message
    elif msg_sent and not msg_received:
        return msg_sent.message
    elif msg_received.timestamp > msg_sent.timestamp:
        return msg_received.message
    elif msg_sent.timestamp > msg_received.timestamp:
        return msg_sent.message


@core.app_template_filter('lastmessageauthor')
def last_message_author(sender):
    msg_received = Message.query.filter_by(
        recipient_id=current_user.id, sender_id=sender.id).order_by(Message.timestamp.desc()).first()
    msg_sent = Message.query.filter_by(
        sender_id=current_user.id, recipient_id=sender.id).order_by(Message.timestamp.desc()).first()
    if msg_received and not msg_sent:
        return msg_received.author
    elif msg_sent and not msg_received:
        return msg_sent.author
    elif msg_received.timestamp > msg_sent.timestamp:
        return msg_received.author
    elif msg_sent.timestamp > msg_received.timestamp:
        return msg_sent.author


@core.app_template_filter('countmessages')
def messages_count(sender):
    messagesreceived = Message.query.filter_by(
        recipient_id=current_user.id, sender_id=sender.id)
    messagessent = Message.query.filter_by(
        sender_id=current_user.id, recipient_id=sender.id)
    messagescount = messagesreceived.count() + messagessent.count()
    if messagescount == 1:
        return (f'{messagescount} convo')
    else:
        return (f'{messagescount} convos')



@core.app_template_filter('newmessages')
def new_message_badge(sender):
    counts = Message.query.filter_by(
        recipient_id=current_user.id, sender_id=sender.id, is_seen=False).count()
    return counts
