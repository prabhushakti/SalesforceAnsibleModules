#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
import requests
import json

def authenticate(module, url, port, user, password):
    session = requests.Session()
    endpoint_login = "{}:{}/api/login".format(url, port)
    session.headers = {'Content-type': 'application/json'}
    auth_data = json.dumps({
        'Username': user,
        'Password': password
    })

    try:
        response = session.post(endpoint_login, data=auth_data)
        response.raise_for_status()
        return session

    except requests.exceptions.RequestException as e:
        module.fail_json(msg="Authentication failed: {}".format(str(e)))

def update_number(module, url, port, session, number):
    endpoint_update = "{}:{}/api/edit/update".format(url, port)
    endpoint_save = "{}:{}/api/edit/save".format(url, port)
    update_number = json.dumps({"Number": number})

    try:
        session.post(endpoint_update, data=update_number)
        response_save = session.post(endpoint_save, data='1')
        response_save.raise_for_status()

        result = {
            'changed': True,
            'status_code': response_save.status_code
        }
        module.exit_json(**result)

    except requests.exceptions.RequestException as e:
        module.fail_json(msg="Update failed: {}".format(str(e)))

def main():
    module_args = {
        'url': {'type': 'str', 'required': True},
        'port': {'type': 'int', 'required': True},
        'user': {'type': 'str', 'required': True},
        'password': {'type': 'str', 'required': True, 'no_log': True},
        'number': {'type': 'str', 'required': True},
    }
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    url = module.params['url']
    port = module.params['port']
    user = module.params['user']
    password = module.params['password']
    number = module.params['number']

    session = authenticate(module, url, port, user, password)
    update_number(module, url, port, session, number)

if __name__ == '__main__':
    main()
