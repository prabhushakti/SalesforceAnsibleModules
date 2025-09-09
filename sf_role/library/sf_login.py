#!/usr/bin/python

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

