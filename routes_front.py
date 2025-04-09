from flask import Blueprint, render_template

import asyncio

from Entity.__all_entities import Note, Tag

front = Blueprint('Front', __name__, static_folder='/static/')

@front.route('/', methods=['GET'])
async def main():
    tags = [
        Tag(name='work'),
        Tag(name='read'),
        Tag(name='personal')
    ]
    notes = [
        Note(user_id=0, text='Sigma', tag_id=0, tag=tags[0]),
        Note(user_id=0, text='Sobolev', tag_id=1, tag=tags[1])
    ]
    return render_template('main.html', title='Home', tags=tags, notes=notes)
# <!-- <link rel="stylesheet" href="{{ url_for('static', path='style.css') }}"> -->