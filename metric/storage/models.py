""" storage models"""

from datetime import datetime
from metrics.metric.storage import db


class Store(db.Model):
    """ storage definition , could be file , db or something else, it is a pointer to actual data"""
    id = db.Column(db.Integer, primary_key=True)
    data_source = db.Column(db.String(100))
    location = db.Column(db.Text)
    storage_type = db.Column(db.String(100))
    business_date = db.Column(db.DateTime)

    def __init__(self, data_source, location, storage_type, business_date=None):
        self.data_source = data_source
        self.location = location
        if business_date is None:
            business_date = datetime.utcnow()
        self.business_date = business_date
        self.storage_type = storage_type

    def __repr__(self):
        return '<Store %r>' % self.data_source
