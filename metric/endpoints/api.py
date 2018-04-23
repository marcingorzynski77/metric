import logging

from flask import request
from flask_restplus import Resource
from metrics.metric.restplus import pagination_arguments, api, metric

log = logging.getLogger(__name__)

ns = api.namespace('metrics', description='Operations related to metrics')


@ns.route('/')
class MetricCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with()
    def get(self):
        """
        Returns list of metrics.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        #posts_query = Post.query
        #posts_page = posts_query.paginate(page, per_page, error_out=False)

        return posts_page

    @api.expect(metric)
    def post(self):
        """
        Creates a new metric.
        """
        create_blog_post(request.json)
        return None, 201


@ns.route('/<string:key>')
@ns.route('/<string:key>/<string:business date 31121999>')
@api.response(404, 'Metric not found.')
class MetricItem(Resource):

    @api.marshal_with(metric)
    def get(self, id):
        """
        Returns a blog post.
        """
        return Post.query.filter(Post.id == id).one()

    @api.expect(blog_post)
    @api.response(204, 'Post successfully updated.')
    def put(self, id):
        """
        Updates a blog post.
        """
        data = request.json
        update_post(id, data)
        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id):
        """
        Deletes blog post.
        """
        delete_post(id)
        return None, 204
