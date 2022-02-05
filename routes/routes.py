from .serializers import *


def initialize_routes(api):
    api.add_resource(GroupApiGet, '/group/<int:group_id>')
    api.add_resource(GroupApiPost, '/group/<int:group_id>')
    api.add_resource(
        GroupApiPut, '/group/<int:group_id>/<string:action>/<int:user_id>'
    )
    api.add_resource(
        GroupApiDelete,
        '/group/<int:group_id>/<string:action>/<int:user_id>'
    )
