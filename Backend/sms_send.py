
from twilio.rest import Client


client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+821066666666",
    from_="+12245430239",
    body="Alert from python")

print(message.sid)
