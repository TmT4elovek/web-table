from flask import Blueprint, render_template, redirect, request

from flask_login import current_user, login_required

from Entity.__all_entities import Tag, User, Note
from Entity import db_session

from forms import NoteForm


front = Blueprint('Front', __name__, static_folder='/static/')

@front.route('/', methods=['GET'])
def main():
    user = current_user if isinstance(current_user, User) else None
    if not user:
        return render_template('main.html', title='Home', tags=[], notes=[], user=user)
    
    session = db_session.create_session()
    
    tags = session.query(Tag).all()
    notes = session.query(User).filter(User.id == user.id).first().all_notes
    
    return render_template('main.html', title='Home', tags=tags, notes=notes, user=user)

@front.route('/create-note', methods=['GET', 'POST'])
@login_required
def create_note():
    session = db_session.create_session()
    tags = session.query(Tag).all()
    tags_labels, tags_ids = list(), list()
    for tag in tags:
        tags_labels.append(tag.name)
        tags_ids.append(tag.id)
    
    form = NoteForm()
    form.tag.choices = list(zip(tuple(tags_ids), tuple(tags_labels)))
    if form.validate_on_submit():
        note = Note(
            user_id=current_user.id,
            tag_id=form.tag.data,
            text=form.text.data
        )
        session.add(note)
        session.commit()
        return redirect('/')
    return render_template('note.html', title='Create note', create='True', form=form, user='not_home')


@front.route('/edit-note/<int:id>')
@login_required
def edit_note(id):
    session = db_session.create_session()
    tags = session.query(Tag).all()
    tags_labels, tags_ids = list(), list()
    for tag in tags:
        tags_labels.append(tag.name)
        tags_ids.append(tag.id)
    
    form = NoteForm()
    form.tag.choices = [tuple(tags_labels), tuple(tags_ids)]
    if request.method == 'GET':
        ...
    if form.validate_on_submit():
        note = Note(
            user_id=current_user.id,
            tag_id=form.tag.data,
            text=form.text.data
        )
        session.add(note)
        session.commit()
        return redirect('/')
    return render_template('note.html', title='Create note', create='True', form=form)