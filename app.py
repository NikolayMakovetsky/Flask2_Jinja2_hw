from flask import Flask, render_template, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import or_
from pathlib import Path
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate

BASE_DIR = Path(__file__).parent

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'quotes.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Для вывода содержимого SQL-запросов в консоли
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
    __tablename__ = "users"
    login = db.Column(db.String(32), unique=True, primary_key=True, nullable=False)
    surname = db.Column(db.String(32), unique=False, nullable=False)
    name = db.Column(db.String(32), unique=False, nullable=False)
    middle_name = db.Column(db.String(32), unique=False, nullable=False)
    birth_date = db.Column(db.String(32), unique=False, nullable=False)
    phone = db.Column(db.String(32), unique=False, nullable=False)


    def to_dict(self):
        return {"login": self.login,
                "surname": self.surname,
                "name": self.name,
                "middle_name": self.middle_name,
                "birth_date": self.birth_date,
                "phone": self.phone}


# Обработка ошибок и возврат значения в виде JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code


@app.get('/') # http://127.0.0.1:5000
def home():
    return render_template("index.html") 


@app.route('/about')
def about():
    return render_template("about.html") 


@app.get('/users')
def users_list():
    users_db = UserModel.query.all()
    entities = list()

    for user_db in users_db:
        entities.append(user_db.to_dict())

    return render_template("users_list.html", **{"entities":entities})


@app.route("/users/<login>")
def user_item(login):
    """Show user profile"""
    item = UserModel.query.get(login)

    if item:
        return render_template("user_info.html", item=item)
    abort(404, f"User with login: {login} not found")

@app.get('/names')
def users_names_list():
    users_db = UserModel.query.all()
    entities = list()

    for user_db in users_db:
        entities.append(user_db.name)

    return render_template("names.html", entities=entities)    


if __name__ == '__main__':
    app.run(debug=True)