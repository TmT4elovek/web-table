from flask import Blueprint, render_template

from Entity.__all_entities import Note, Tag
from Entity import db_session

front = Blueprint('Front', __name__, static_folder='/static/')

@front.route('/', methods=['GET'])
async def main():
    session = db_session.create_session()

    tags = session.query(Tag).all()
    notes=[]
    

    return render_template('main.html', title='Home', tags=tags, notes=notes)