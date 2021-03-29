from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
app = Flask(__name__)
client = app.test_client()

engine = create_engine('sqlite:///db.sqlite', echo=False)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.query = session.query_property()

from functional.Models import *

Base.metadata.create_all(bind=engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from functional.Courier.RoutesCourier import couriers
from functional.Orders.RouteOrder import orders

app.register_blueprint(couriers)
app.register_blueprint(orders)
