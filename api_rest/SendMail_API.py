import sendgrid
import os
import sys

pa = sys.argv[1]

sg = sendgrid.SendGridAPIClient('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')
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "miso.uniandes.estudiante@gmail.com"
        }
      ],
      "subject": "Task already processed"
    }
  ],
  "from": {
    "email": "miso.uniandes.estudiante@gmail.com"
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