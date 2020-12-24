from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from mytravelplan import db, messages
from mytravelplan.messages.forms import MessageForm, MessageAllForm
from mytravelplan.models import Post, Comment, Message, User
from mytravelplan.posts.forms import PostForm, CommentForm
from mytravelplan.posts.utils import save_picture

messages = Blueprint('messages', __name__)


# In that file all the routes of the posts at the website, here is all the logic and functionality of the posts
# and here is the templates that user sees that belong to posts

# Return 3 counters of messages, [0] = inboxMessagesCounter [1] = unreadMessagesCounter [2] = sentMessagesCounter
@login_required
def messages_counters():
    msg_counters = []
    inboxMessagesCounter = Message.query.filter_by(receiver=current_user.username, deletedByReceiver=False).count()
    msg_counters.append(inboxMessagesCounter)
    unreadMessagesCounter = Message.query.filter_by(receiver=current_user.username, readed=False,
                                                    deletedByReceiver=False).count()
    msg_counters.append(unreadMessagesCounter)
    sentMessagesCounter = Message.query.filter_by(owner=current_user.username, deletedByOwner=False).count()
    msg_counters.append(sentMessagesCounter)
    return msg_counters



# sent messages
@messages.route('/sent')
@login_required
def sent_messages():
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(owner=current_user.username, deletedByOwner=False).order_by(
        Message.date_posted.desc()).paginate(
        page=page, per_page=5)
    return render_template('sent_messages.html', messages=messages, msg_counters=msg_counters)


# inbox of messages
@messages.route('/inbox')
@login_required
def inbox():
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(receiver=current_user.username, deletedByReceiver=False).order_by(
        Message.date_posted.desc()).paginate(
        page=page, per_page=5)
    return render_template('inbox.html', messages=messages, msg_counters=msg_counters)


# unread messages
@messages.route('/unreaded')
@login_required
def unread_messages():
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(receiver=current_user.username, readed=False, deletedByReceiver=False).order_by(
        Message.date_posted.desc()).paginate(
        page=page, per_page=5)
    return render_template('unread_messages.html', messages=messages, msg_counters=msg_counters)


# Shows specific message
@messages.route("/message/<int:message_id>", methods=['GET', 'POST'])
@login_required
def message(message_id):
    message = Message.query.get_or_404(message_id)
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()

    if current_user.username == message.receiver:
        message.readed = True
        db.session.commit()
        return render_template('message.html', message=message, msg_counters=msg_counters)
    if current_user.username == message.owner:
        return render_template('message.html', message=message, msg_counters=msg_counters)
    else:
        abort(403)


# delete message
@messages.route("/message/<int:message_id>/delete/", methods=['GET', 'POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if current_user.username == message.receiver:
        message.deletedByReceiver = True
        db.session.commit()
        return redirect(url_for('messages.inbox'))
    if current_user.username == message.owner:
        message.deletedByOwner = True
        db.session.commit()
        return redirect(url_for('messages.inbox'))
    else:
        abort(403)


# Shows form for creation of a new message
@messages.route("/message/new/<string:receiver>/", methods=['GET', 'POST'])
@login_required
def new_message(receiver):
    form = MessageForm()
    # Generic functionality
    # Messages counters
    msg_counters = messages_counters()

    if form.validate_on_submit():
        if receiver == 'Name of receiver here..':
            receiver = form.receiver.data
        message = Message(subject=form.subject.data, content=form.content.data, owner=current_user.username,
                          receiver=receiver)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('messages.inbox'))
    form.receiver.data = receiver
    return render_template('create_message.html', form=form, msg_counters=msg_counters)



# Shows form for creation a new message to all
@messages.route("/message/new/all/", methods=['GET', 'POST'])
@login_required
def new_message_to_all():
    if current_user.admin_permissions == 1:
        form = MessageAllForm()
        # Generic functionality
        # Messages counters
        msg_counters = messages_counters()

        if form.validate_on_submit():
            users = User.query.all()
            for user in users:
                message = Message(subject=form.subject.data, content=form.content.data, owner=current_user.username, receiver=user.username)
                db.session.add(message)
            db.session.commit()
            flash('Your message has been sent!', 'success')
            return redirect(url_for('messages.inbox'))
        return render_template('create_message_all.html', form=form, msg_counters=msg_counters)
    else:
        abort(403)