""" rest plus handler"""
import logging

from flask_restplus import Api, reqparse
from metrics.metric.configuration import Configuration
from flask_restplus import fields

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Metrics API',
          description='Metrics RestPlus powered API')

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')


metric = api.model('Metric', {
    'key': fields.Integer(readOnly=True, description='TThe metric namespace'),
    'business_date': fields.DateTime,
    'payload': fields.String(attribute='Metric content'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message, e)

    if not Configuration.flask_debug:
        return {'message': message}, 500
