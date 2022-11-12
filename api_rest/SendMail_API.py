import sendgrid
import os
import sys

pa = sys.argv[1]

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "toolcloudconversion@gmail.com"
        }
      ],
      "subject": "Task already processed"
    }
  ],
  "from": {
    "email": "toolcloudconversion@gmail.com"
  },
  "content": [
    {
      "type": "text/plain",
      "value": pa
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)
