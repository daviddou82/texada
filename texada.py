from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import cerberus

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///texada.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class table1(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    event_id = db.Column(db.Integer, unique=True)
    description = db.Column(db.String(120))
    datetime = db.Column(db.String(120))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    elevation = db.Column(db.Integer)

    def __init__(self,index,event_id, description,datetime,longitude,latitude,elevation):
        self.index =index
        self.event_id = event_id
        self.description = description
        self.datetime = datetime
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation


class table1Schema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('index','event_id', 'description','datetime','longitude','latitude','elevation')


table1_schema = table1Schema()
table1_schemas = table1Schema(many=True)


# endpoint to create new equipment
@app.route("/equipment", methods=["POST"])
def add_equipment():
    index = request.json['index']
    event_id = request.json['event_id']
    description = request.json['description']
    datetime = request.json['datetime']
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    elevation = request.json['elevation']

    schema = {'event_id': {'type': 'integer'},
              'description': {'type': 'string'},
              'datetime': {'type': 'string'},
              'longitude': {'type': 'float'},
              'latitude': {'type': 'float'},
              'elevation': {'type': 'integer'}}
    v = cerberus.Validator(schema)

    flag1 = v.validate({'event_id': event_id})
    flag2 = v.validate({'description': description})
    flag3 = v.validate({'datetime': datetime})
    flag4 = v.validate({'longitude': longitude})
    flag5 = v.validate({'latitude': latitude})
    flag6 = v.validate({'elevation': elevation})

    if flag1 == flag2 == flag3 == flag4 == flag5 == flag6 is True:

        new_equipment = table1(index, event_id, description,datetime,longitude,latitude,elevation)
        #
        db.session.add(new_equipment)
        db.session.commit()
        print (new_equipment)
        all_equipment = table1.query.all()
        result = table1_schemas.dump(all_equipment)
        return jsonify(result.data)


@app.route('/')
def hello_world():
    return 'Hello, World!'

# endpoint to show all equipment
@app.route("/equipment", methods=["GET"])
def get_equipment():
    all_equipment = table1.query.all()
    result = table1_schemas.dump(all_equipment)
    return jsonify(result.data)

# endpoint to get equipment detail by id
@app.route("/equipment/<event_id>", methods=["GET"])
def equipment(event_id):
    select_equipment = table1.query.get(event_id)
    return table1_schema.jsonify(select_equipment)


# endpoint to update equipment
@app.route("/equipment/<event_id>", methods=["PUT"])
def equipment_update(event_id):
    equipment = table1.query.get(event_id)
    event_id = request.json['event_id']
    elevation = request.json['elevation']

    table1.elevation = elevation
    table1.event_id =event_id

    db.session.commit()
    return table1_schema.jsonify(table1)


# endpoint to delete equipment
@app.route("/equipment/<event_id>", methods=["DELETE"])
def equipment_delete(event_id):
    equipment = table1.query.get(event_id)
    db.session.delete(equipment)
    db.session.commit()

    return table1_schema.jsonify(table1)

if __name__ == '__main__':
    app.run(debug=True)