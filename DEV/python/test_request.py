import requests
r = requests.get('http://localhost:8668/v2/notify')

url = 'http://localhost:8668/v2/notify'

headers = {
    'content-type': 'application/json',
    'fiware-service': 'opcua_car',
    'fiware-servicepath': '/demo'
    }

# payload = {'some': 'data'}

# r = requests.options(url, headers=headers)
r = requests.post(url, headers=headers)
# r = requests.get(url, headers=headers)

# r = requests.post(url, data=json.dumps(payload), headers=headers)
# r = requests.get(url, data=json.dumps(payload), headers=headers)

# # r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
print(r.status_code)
# 200
print(r.headers)

# 'Content-Type: application/json', 'fiware-service: opcua_car', 'fiware-servicepath: /demo'
# 'application/json; charset=utf8'
print(r.encoding)
# 'utf-8'
print(r.text)
# '{"authenticated": true, ...'
# print(r.json())
# {'authenticated': True, ...}