
from twilio.rest import Client

account_sid = 'AC9da53aa4db8eb8842adea4cb74712408'
auth_token = '9dcb0974023e4c25447d98c19e17073d'
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+821066666666",
    from_="+12245430239",
    body="Alert from python")

print(message.sid)
