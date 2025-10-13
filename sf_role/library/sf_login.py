#!/usr/bin/python

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
        required: false
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


from ansible.module_utils.basic import AnsibleModule
import requests

def salesforce_login(client_id, client_secret, username, password, security_token):
    url = "https://login.salesforce.com/services/oauth2/token"
    payload = {
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password + security_token
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None, response.text

def main():
    module_args = dict(
        client_id=dict(type='str', required=True),
        client_secret=dict(type='str', required=True, no_log=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        security_token=dict(type='str', required=True, no_log=True)
    )

    result = dict(
        changed=False,
        access_token=None,
        instance_url=None,
        error=None
    )

    module = AnsibleModule(argument_spec=module_args)

    client_id = module.params['client_id']
    client_secret = module.params['client_secret']
    username = module.params['username']
    password = module.params['password']
    security_token = module.params['security_token']

    token_info, error = salesforce_login(client_id, client_secret, username, password, security_token)

    if token_info:
        result['access_token'] = token_info.get('access_token')
        result['instance_url'] = token_info.get('instance_url')
    else:
        result['error'] = error

    module.exit_json(**result)

if __name__ == '__main__':
    main()

