from flask import Flask

from Entity import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_table_project_yml'

db_session.global_init('database.sqlite')

@app.route('/', methods=['GET'])
async def main():
    return 'test'


if __name__ == '__main__':
    app.run('127.0.0.1', '8080', debug=True)