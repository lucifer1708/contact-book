from flask import Flask, jsonify, request
from faker import Faker
from models import db, Contact, Company

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '85c38682ec6f65b1b510a473baa02612'
# app.config['DEBUG'] = True


print("hello")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()
    # gen_data()
    db.session.commit()


@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.json
    name = data['name']
    mobile_number = data['mobile_number']
    address = data['address']
    email = data['email']
    instagram_handle = data['instagram_handle']
    company_names = data.get('companies', [])
    companies = []
    for company_name in company_names:
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
        companies.append(company)

    contact = Contact(name=name, mobile_number=mobile_number, address=address,
                      email=email, instagram_handle=instagram_handle, companies=companies)
    # Add the contact to the database
    db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'Contact created successfully.'}), 201


@app.route('/fake', methods=['GET'])
def generate_fake():
    for _ in range(100):
        fake = Faker()
        name = fake.name()
        mobile_number = fake.phone_number()
        address = fake.address()
        email = fake.email()
        instagram_handle = fake.user_name()
        company_names = [fake.company(), fake.company()]
        companies = []
        for company_name in company_names:
            company = Company.query.filter_by(name=company_name).first()
            if not company:
                company = Company(name=company_name)
                db.session.add(company)
            companies.append(company)

        contact = Contact(name=name, mobile_number=mobile_number, address=address,
                          email=email, instagram_handle=instagram_handle, companies=companies)
        # Add the contact to the database
        db.session.add(contact)
    db.session.commit()
    return jsonify({'message': 'fake enteries have been done'}), 201


@app.route('/', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    result = []
    for contact in contacts:
        contact_dict = {
            'id': contact.id,
            'name': contact.name,
            'mobile_number': contact.mobile_number,
            'address': contact.address,
            'email': contact.email,
            'instagram_handle': contact.instagram_handle,
            # Iterate over list of associated companies
            'companies': [company.name for company in contact.companies]
        }
        result.append(contact_dict)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
