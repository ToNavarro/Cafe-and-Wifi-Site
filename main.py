from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from random import choice
import os
from dotenv import load_dotenv, find_dotenv
from forms import CafeForm, ContactForm
from flask_bootstrap import Bootstrap4

# Find .env file
dotenv_path = find_dotenv()
# Load .env file entries as environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
db = SQLAlchemy()
db.init_app(app)
Bootstrap4(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    random_cafe = choice(result.scalars().all())
    return jsonify(cafe={"name": random_cafe.name,
                         "id": random_cafe.id,
                         "coffee_price": random_cafe.coffee_price,
                         "map_url": random_cafe.map_url,
                         "img_url": random_cafe.img_url,
                         "has_sockets": random_cafe.has_sockets,
                         "has_wifi": random_cafe.has_wifi,
                         "seats": random_cafe.seats,
                         "has_toilet": random_cafe.has_toilet,
                         "can_take_calls": random_cafe.can_take_calls,
                         "location": random_cafe.location,
                         })


@app.route("/cafes")
def get_all():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    # return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])
    return render_template("cafes.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/search")
def search():
    loc = request.args.get("loc")
    loc_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == loc).order_by(Cafe.name)).scalars().all()
    if loc_cafes:
        return jsonify(cafe=[cafe.to_dict() for cafe in loc_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"}), 404


"""
@app.route('/add', methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})
"""


@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    cafe_to_up = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    new_price = request.args.get("new_price")
    if cafe_to_up:
        cafe_to_up.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route('/report-closed/<int:cafe_id>', methods=["DELETE"])
def report_closed(cafe_id):
    key = request.args.get("api-key")
    if key == "TopSecretAPIKey":
        cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = f"{form.cafe.data}\n\n{form.location.data}\n\n{form.description.data}"
        print(new_cafe)
        flash("Cafe successfully suggested. Thanks for your collaboration.")
        # with open('cafe-data.csv', "a", encoding='utf-8') as csv_file:
        #     csv_file.write(f"\n{new_row}")
        # TODO: Configure where to store the messages so admin can check and add Cafe to Database.
        return redirect(url_for('add_cafe'))
    return render_template('book.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)


# Bootstrap template from:
# https://themewagon.com/themes/free-bootstrap-4-html5-restaurant-website-template-feane/
