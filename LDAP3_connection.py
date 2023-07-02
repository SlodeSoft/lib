from flask_ldap3_login import LDAP3LoginManager
from json import dumps


class ldap3:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def ldap3_test(self):
        config = dict()

        # Setup LDAP Configuration Variables. Change these to your own settings.
        # All configuration directives can be found in the documentation.

        # Hostname of your LDAP Server
        config['LDAP_HOST'] = '192.168.3.3'
        # Base DN of your directory
        config['LDAP_BASE_DN'] = 'dc=home,dc=lab,dc=local'
        # Users DN to be prepended to the Base DN
        config['LDAP_USER_DN'] = 'ou=LAB'
        # Groups DN to be prepended to the Base DN
        config['LDAP_GROUP_DN'] = 'ou=LAB'
        # ...
        config['LDAP_USER_SEARCH_SCOPE'] = 'SUBTREE'
        config['LDAP_GROUP_SEARCH_SCOPE'] = 'SUBTREE'
        # ...
        config['LDAP_BIND_DIRECT_SUFFIX'] = '@home.lab.local'
        # The RDN attribute for your user schema on LDAP
        config['LDAP_USER_RDN_ATTR'] = 'cn'
        # The Attribute you want users to authenticate to LDAP with.
        config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'
        # The Attributes you want to return about user
        config['LDAP_GET_USER_ATTRIBUTES'] = ("mail", "givenName", "sn")
        # The Username to bind to LDAP with
        config['LDAP_BIND_USER_DN'] = 'CN=bind bind,OU=LAB,DC=home,DC=lab,DC=local'
        # The Password to bind to LDAP with
        config['LDAP_BIND_USER_PASSWORD'] = 'never'
        # Setup a LDAP3 Login Manager.
        ldap_manager = LDAP3LoginManager()

        # Init the mamager with the config since we aren't using an app
        ldap_manager.init_config(config)
        # Check if the credentials are correct

        response = ldap_manager.authenticate_direct_credentials(username=self.user,
                                                                password=self.password)
        reponse_json = {"user_dn": dict(item.split("=") for item in response.user_dn.split(",")),
                        "status": response.status.name,
                        "user_id": response.user_id,
                        "user_info": response.user_info,
                        "user_groups": response.user_groups}
        return reponse_json

    def verify_login(self, data):
        if data['user_dn']['OU'] == "groupA":
            data.update({'status_verify': 'success'})
            return data
        else:
            data.update({'status_verify': 'fail'})
            return data


if __name__ == "__main__":
    user_auth = ldap3(user='bind', password='never')
    user_verify = user_auth.verify_login(user_auth.ldap3_test())
    print(user_verify)
