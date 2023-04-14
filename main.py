from flask import Flask, jsonify, request
from faker import Faker
from models import db, Contact, Company
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Creating Database
with app.app_context():
    # db.drop_all()
    db.create_all()
    # gen_data()
    db.session.commit()


@app.route('/create', methods=['POST'])
def create_contact():
    # Function to Create a contact.
    data = request.json
    name = data['name']
    mobile_number = data['mobile_number']
    address = data['address']
    email = data['email']
    instagram_handle = data['instagram_handle']
    company_names = data.get('companies', [])
    if not any([mobile_number, email, instagram_handle]):
        return jsonify({'message': 'At least one of mobile_number, email or instagram_handle is required'}), 400
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


@app.route('/contacts', methods=['GET'])
def get_contact_by_search_term():
    # Function to get the contacts by searching using params.
    search_term = request.args.get('search')
    contact = Contact.query.filter_by(mobile_number=search_term).first()
    if not contact:
        contact = Contact.query.filter_by(email=search_term).first()
    if not contact:
        contact = Contact.query.filter_by(instagram_handle=search_term).first()
    if not contact:
        return jsonify({'message': 'No contact found for search term.'}), 404
    contact_dict = {
        'id': contact.id,
        'name': contact.name,
        'mobile_number': contact.mobile_number,
        'address': contact.address,
        'email': contact.email,
        'instagram_handle': contact.instagram_handle,
        'companies': [company.name for company in contact.companies]
    }
    return jsonify(contact_dict), 200


@app.route('/contacts/company')
def get_contacts_by_company():
    # Function to get contact by company name by passing name in params
    company_name = request.args.get('name')
    company = Company.query.filter_by(name=company_name).first()

    if company:
        contacts = company.contacts
        response = []
        for contact in contacts:
            response.append({
                'id': contact.id,
                'name': contact.name,
                'mobile_number': contact.mobile_number,
                'address': contact.address,
                'email': contact.email,
                'instagram_handle': contact.instagram_handle,
                # Iterate over list of associated companies
                'companies': [company.name for company in contact.companies]
            })
        return jsonify(response)
    else:
        return jsonify({'message': 'Company not found.'}), 404


@app.route('/', methods=['GET'])
def get_contacts():
    # Get All Contacts
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


@app.route('/contacts/<string:field>/<string:value>', methods=['PUT'])
def update_contact(field, value):
    # Get the contact with the specified field and value
    if field == 'mobile':
        contact = Contact.query.filter_by(mobile_number=value).first()
    elif field == 'email':
        contact = Contact.query.filter_by(email=value).first()
    elif field == 'instagram':
        contact = Contact.query.filter_by(instagram_handle=value).first()
    else:
        return jsonify({'message': 'Invalid field parameter'}), 400

    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    data = request.get_json()
    contact.name = data['name']
    contact.mobile_number = data['mobile_number']
    contact.email = data['email']
    contact.instagram_handle = data['instagram_handle']
    contact.companies = []

    company_names = data.get('companies', [])
    for company_name in company_names:
        company = Company.query.filter_by(name=company_name).first()
        if company:
            contact.companies.append(company)
    db.session.commit()
    contact_dict = {
        'id': contact.id,
        'name': contact.name,
        'mobile_number': contact.mobile_number,
        'address': contact.address,
        'email': contact.email,
        'instagram_handle': contact.instagram_handle,
        'companies': [company.name for company in contact.companies]}
    return jsonify(contact_dict), 200


@app.route('/fake', methods=['GET'])
def generate_fake():
    # Generate fake  data and commit to database.
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


if __name__ == '__main__':
    app.run(debug=True)
