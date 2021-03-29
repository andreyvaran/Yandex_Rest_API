import sqlalchemy as db

from functional import Base


class Courier(Base):
    __tablename__ = 'courier'

    courier_id = db.Column(db.Integer, primary_key=True)
    courier_type = db.Column(db.VARCHAR(4), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    regions = db.Column(db.JSON)
    working_hours = db.Column(db.JSON)
    current_time = db.Column(db.String, default='')
    assign_time = db.Column(db.String, default='')
    current_orders = db.Column(db.JSON, default=[])
    delivery = db.Column(db.Integer, default=0)
    selary_str = db.Column(db.String, default='')

class Order(Base):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    region = db.Column(db.Integer, nullable=False)
    delivery_hours = db.Column(db.JSON)
    id_courier = db.Column(db.Integer , default= -1)
    delivety_time = db.Column(db.Integer, default=0)

