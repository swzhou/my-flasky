from . import main
from datetime import datetime
from flask import request, session, url_for, render_template, redirect,current_app
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_mail

@main.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_mail(current_app.config['FLASKY_ADMIN'],
                          'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           user_agent=user_agent,
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))
