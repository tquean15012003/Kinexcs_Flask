from flask_restx import Namespace, Resource, fields, reqparse
from ..models.customers import Customer
from http import HTTPStatus
from ..utils import db
from flask import request

customer_namespace = Namespace('Customer', description="Customer-related APIs")

customer_model = customer_namespace.model(
    'Customer',{
        'id':fields.Integer(description="Customer ID"),
        'name':fields.String(description="Customer name", required=True),
        'dob':fields.Date(description="Customer date of birth", required=True)
    }
)

parser = reqparse.RequestParser()
parser.add_argument('number', type=int, help='Not required')

@customer_namespace.route('')
class CustomerGet(Resource):
    @customer_namespace.expect(parser)
    @customer_namespace.marshal_list_with(customer_model, mask=False)
    def get(self):
        """
            Leave "number" query blank to retrieve all customers || input "number" query to retrieve {number} youngest customers
        """
        
        number = request.args.get('number')

        if (number is None):
            customers = Customer.query.order_by(Customer.id.asc()).all()
            return customers, HTTPStatus.OK
        else:
            customers = Customer.query.order_by(Customer.dob.desc()).limit(number).all()
            return customers, HTTPStatus.OK

        

@customer_namespace.route('/create')
class CustomerCreate(Resource):
    @customer_namespace.expect(customer_model)
    @customer_namespace.marshal_with(customer_model, mask=False)
    def post(self):
        """
            Create a new customer
        """
        
        data = customer_namespace.payload

        new_customer = Customer(
            name = data['name'],
            dob = data['dob']
        )

        new_customer.save()

        return new_customer, HTTPStatus.CREATED


@customer_namespace.route('/<int:id>')
@customer_namespace.doc(params={'id': 'Customer id'})
class CustomerCreate(Resource):
    @customer_namespace.marshal_with(customer_model, mask=False)
    def get(self, id):
        """
            Retrieve a customer by customer id
        """
        
        customer = Customer.get_by_id(id)

        return customer, HTTPStatus.OK

    @customer_namespace.expect(customer_model)
    @customer_namespace.marshal_with(customer_model, mask=False)
    def put(self, id):
        """
            Update a customer by customer id
        """
        
        customer_to_update = Customer.get_by_id(id)

        data = customer_namespace.payload

        customer_to_update.name = data['name']

        customer_to_update.dob = data['dob']

        db.session.commit()

        return customer_to_update, HTTPStatus.OK

    @customer_namespace.marshal_with(customer_model, mask=False)
    def delete(self, id):
        """
            Delete a customer by cusomter id
        """
        
        customer_to_delete = Customer.get_by_id(id)

        customer_to_delete.delete()

        return customer_to_delete, HTTPStatus.NO_CONTENT
