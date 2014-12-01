def export_csv(context, data_dict):
    '''Check if the user has admin rights in some org'''
    from ckan import new_authz
    user_name = context.get('user')
    if user_name:
        check = new_authz.has_user_permission_for_some_org(user_name, 'admin')
        if check:
            return {'success': True}
    return {'success': False}
