import os

import aiosmtpd.handlers
import aiosmtplib
import email
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.environ["SMTP_PORT"])

class TransactionalHandler(aiosmtpd.handlers.AsyncMessage):
    async def handle_message(self, message: email.message.EmailMessage):
        transactional_mail = False
        if message.get("Remove-List-Unsubscribe", None):
            del message["List-Unsubscribe"]
            transactional_mail = True

        del message['X-Peer']
        del message['X-MailFrom']
        del message['X-RcptTo']

        await aiosmtplib.send(message, hostname=SMTP_HOST, port=SMTP_PORT)

        if transactional_mail:
            log.info(f'Transactional Mail has been sent to {",".join(message.get_all("to", []))}')
        else:
            log.info(f'Non-Transactional Mail has been sent to {",".join(message.get_all("to", []))}')
