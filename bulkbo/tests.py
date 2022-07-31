from django.test import TestCase
import requests

to = '85566362218,855663622182,85566362218,85566362218,85566362219,8855663622120,8855663622181'
x = requests.get(f'http://gateway.sms77.io/api/sms?p=w8f7Cjk6jKEH7NkyAiuNZ4PQn25wXbjGINLqKW7adpeaQpunakzV276X3Zn3jgS9&to={to}&text=Test+SMS&from=SMS&debug=1&json=1')
y = x.json()
for i in y['messages']:
    print(i)


