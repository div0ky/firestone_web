from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required

from app.admin import bp
from app import db
from app.admin.forms import LoginForm, ChangelogForm
from app.models import License, User, Post


@bp.route('/list')
@login_required
def list_active_bots():
    _licenses = License.query.order_by(License.last_seen.asc()).all()
    if _licenses is not None:
        active = []
        inactive = []
        for _license in _licenses:
            if _license.last_seen + timedelta(minutes=5) >= datetime.utcnow():
                active.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number, 'last_seen': _license.last_seen,
                            'current_ip': _license.current_ip, 'all_ips': _license.all_ips, 'age': 'active'})
            else:
                inactive.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number,
                            'last_seen': _license.last_seen + timedelta(minutes=5), 'current_ip': _license.current_ip,
                            'all_ips': _license.all_ips, 'age': 'inactive'})

    return render_template('list.html', active=active, inactive=inactive)

@bp.route('/changelog', methods=['GET', 'POST'])
@login_required
def post_changelog():
    form = ChangelogForm()
    if form.validate_on_submit():
        post = Post(subject=form.subject.data, summary=form.summary.data, change_type=form.change_type.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published!')
        return redirect(url_for('main.changelog'))
    return render_template('/admin/changelog.html', form=form)

@bp.route('/delete/<post>', methods=['POST'])
@login_required
def delete_post(post):
    post = Post.query.get(post)
    db.session.delete(post)
    db.session.commit()
    flash('Deleted record!')
    return redirect(url_for('main.changelog'))

@bp.route('/edit/<post>', methods=['GET', 'POST'])
@login_required
def edit_post(post):
    existing_post = Post.query.get(post)
    form = ChangelogForm(formdata=request.form, obj=existing_post)
    if form.validate_on_submit():
        existing_post.subject = form.subject.data
        existing_post.summary = form.summary.data
        existing_post.change_type = form.change_type.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.changelog'))
    elif request.method == 'GET':
        form.subject.data = existing_post.subject
        form.summary = existing_post.summary
        form.change_type = existing_post.change_type
    return render_template('/admin/changelog.html', form=form)