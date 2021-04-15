from datetime import datetime
from os import path

from flask import current_app
from PIL import Image


def cropper(image):
    full_width, full_height = image.size
    width = min(image.size)
    height = min(image.size)
    return image.crop(((full_width - width) // 2, (full_height - height) // 2, (full_width + width) // 2, (full_height + height) // 2))


def save_picture(username, form_picture):
    _, f_ext = path.splitext(form_picture.filename)
    picture_fn = username + f_ext
    picture_path = path.join(current_app.root_path,
                             'static/profilepics', picture_fn)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img = cropper(img).resize(output_size, Image.LANCZOS)
    img.save(picture_path)
    return picture_fn


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
