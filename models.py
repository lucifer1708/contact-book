from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

# SQLite Database init
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

contact_company_association = db.Table('contact_company_association',
                                       db.Column('contact_id', db.Integer, db.ForeignKey(
                                           'contact.id'), primary_key=True),
                                       db.Column('company_id', db.Integer, db.ForeignKey(
                                           'company.id'), primary_key=True)
                                       )


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    mobile_number = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    instagram_handle = db.Column(db.String(50), unique=True, nullable=False)
    companies = db.relationship(
        'Company', secondary=contact_company_association, backref=db.backref('contacts', lazy=True))


def __repr__(self):
    return f'<Contact Name {self.name}>'


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Company Name {self.name}>'
