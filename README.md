# Installation
```
pip install -r requirements.txt
```
# Usage
```
flask --app main run
```

# Api end points

```
/[GET]--> for getting all contacts.
/create[POST]--> for creating a contact.
/contacts[GET]--> searching for contact using search param.
/contacts/company[GET]--> get contact by company name by passing name param.
/contacts/<field>/<value>[PUT]--> get the contact with value and field then edit it with json.
/fake[GET]--> generate fake data for database.
```

Readme is not well written due to time constraint.

