# Copyright: (c) 2025, Prabhushakti H. <prabhu@duck.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: sf_login

short_description: Logins into org
version_added: "1.0.0"

description: sf_login can authenticate with specified salesforce org.

options:
    client_id:
        description: client id.
        required: for jwt 
        type: str
    client_secret:
        description: It is recommeded to use base64 encoded
        required: false
        type: str
    username:
        description: Salesforce user name.
            - Required if you're not using jwt based authentication.
            - enter your username
        required: false
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Prabhushakti H.(@prabhushakti)
'''

EXAMPLES = r'''
# JWT Login
- name: Login using json web token
  sf_login:
    client_id: XXXX
    client_key: file.crt

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: if defined
    sample: 'failed'
message:
    description: The output message that the test module generates.
    type: json
    returned: always
    sample: '{ success }'
'''

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
