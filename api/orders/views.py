from flask_restx import Namespace, Resource, reqparse, fields
from ..models.orders import Order
from ..models.customers import Customer
from flask import request, jsonify
from http import HTTPStatus
from ..utils import db
import json

order_namespace = Namespace('Order', description="Order-related APIs")

order_model = order_namespace.model(
    'Order',{
        'id':fields.Integer(description="Customer ID"),
        'item_name':fields.String(description="Item name", required=True),
        'item_price':fields.Float(description="Item price", required=True),
        'customer_id':fields.Integer(description="Customer ID", required=True),
        'created_at':fields.DateTime(description="Created at", required=True),
    }
)

@order_namespace.route('/<int:id>')
@order_namespace.doc(params={'id': 'Order id'})
class OrderUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model, mask=False)
    def get(self, id):
        """
            Retrieve a order by order id
        """

        order = Order.get_by_id(id)
        return order, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model, mask=False)
    def put(self, id):
        """
            Update an order by order id
        """

        order_to_update = Order.get_by_id(id)
        
        data  = order_namespace.payload

        order_to_update.item_name = data['item_name'] 

        order_to_update.item_price = data['item_price']

        order_to_update.customer_id = data['customer_id']

        db.session.commit()

        return order_to_update, HTTPStatus.OK
        
    @order_namespace.marshal_with(order_model, mask=False)
    def delete(self, id):
        """
            Delete an order by order id
        """

        order_to_delete = Order.get_by_id(id)

        order_to_delete.delete()

        return order_to_delete, HTTPStatus.NO_CONTENT

parser = reqparse.RequestParser()
parser.add_argument('customer_id', type=int, help='Not required')
@order_namespace.route('')
class OrderGetByCustomerID(Resource):
    @order_namespace.expect(parser)
    @order_namespace.marshal_list_with(order_model, mask=False)
    def get(self):
        """
            Leave "customer_id" query blank to retrieve all orders || Input "customer_id" query to retrieve all orders for a customer by customer id
        """

        customer_id = request.args.get('customer_id')

        if (customer_id is None):
            orders = Order.get_all()
            return orders, HTTPStatus.OK
        else:
            orders = Order.query.filter_by(customer_id=customer_id).all()
            return orders, HTTPStatus.OK
    
    @order_namespace.expect(order_model)
    @order_namespace.marshal_list_with(order_model, mask=False)
    def post(self):
        """
            Create a new order
        """

        data = order_namespace.payload

        new_order = Order(
            item_name = data['item_name'],
            item_price = data['item_price'],
            customer_id = data['customer_id']

        )

        new_order.save()

        return new_order, HTTPStatus.CREATED

