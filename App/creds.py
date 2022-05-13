# vault token create -id="tokenSecretHere" -display-name="app-vault-token" -orphan -policy=appname -renewable=true -ttl=999999h -no-default-policy

# # This section grants all access on "secret/*". Further restrictions can be
# # applied to this broad policy, as shown below.
# path "secret/appname" {
#   capabilities = ["read", "list"]
# }


__hashi_vault_token__ = 'tokenSecretHere'
__hashi_vault_URL__ = 'http://localhost'

def get_vault_kv() -> dict:
    import hvac
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    client = hvac.Client(url=__hashi_vault_URL__, verify=False)
    client.token = __hashi_vault_token__
    client.secrets.kv.default_kv_version = '2'

    return client.secrets.kv.read_secret_version(mount_point='secret', path='appname')

read_response = get_vault_kv()

username = read_response['data']['data']['username']
password = read_response['data']['data']['password']