from flask import Blueprint, render_template, redirect, request, abort

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
    form = NoteForm()
    
    if not form.tag.choices:
        session = db_session.create_session()
        tags = session.query(Tag).all()
        form.tag.choices = [(tag.id, tag.name) for tag in tags]

    if form.validate_on_submit():
        session = db_session.create_session()

        note = Note(
            user_id=current_user.id,
            tag_id=form.tag.data,
            text=form.text.data
        )
        session.add(note)
        session.commit()
        return redirect('/')
    return render_template('note.html', title='Create note', create=True, form=form, user='not_home')

@front.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    form = NoteForm()
    
    session = db_session.create_session()
    tags = session.query(Tag).all()
    form.tag.choices = [(tag.id, tag.name) for tag in tags]
    
    note = session.query(Note).filter(Note.id == id, Note.creator == current_user).first()
    if not note:
        return abort(404)
    
    if request.method == 'GET':
        form.process(data={'tag': note.tag_id})
        form.text.data = note.text
    
    if form.validate_on_submit():
        note.tag_id = form.tag.data
        note.text = form.text.data
        session.commit()
        return redirect('/')
    
    return render_template('note.html', title='Edit note', create=False, form=form, id=id, user='not_home')


@front.route('/delete-note/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    session = db_session.create_session()
    note = session.query(Note).filter(Note.id == id, Note.creator == current_user).first()
    if note:
        session.delete(note)
        session.commit()
        return redirect('/')
    else:
        return abort(404)