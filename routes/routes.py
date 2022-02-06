from routes.serializers import *


def initialize_routes(api):
    api.add_resource(GroupApiGet, '/get_info/<int:group_id>')
    api.add_resource(GroupApiPost, '/add_group/<int:group_id>')
    api.add_resource(
        GroupApiPut, '/modify/<int:group_id>/<string:action>/<int:user_id>', 

    )
    api.add_resource(
        GroupApiDelete,
        '/remove/<int:group_id>/<string:action>/<int:user_id>',
    )
    api.add_resource(UserApiGet, '/user_info/<int:user_id>')
    api.add_resource(UserApiPost, '/add_user/<int:user_id>')
    api.add_resource(UserApiPut, '/modify_user/<int:user_id>')
    

