
from twilio.rest import Client


client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+",
    from_="+",
    body="Alert from python")

print(message.sid)
