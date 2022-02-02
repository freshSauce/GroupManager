from .serializers import *


def initialize_routes(api):
    api.add_resource(GroupApiGet, '/group/<string:group_id>')
    api.add_resource(GroupApiPost, '/group/<string:group_id>')
    api.add_resource(
        GroupApiPut, '/group/<string:group_id>/<string:action>/<string:user_id>'
    )
    api.add_resource(
        GroupApiDelete,
        '/group/<string:group_id>/<string:action>/<string:user_id>'
    )
