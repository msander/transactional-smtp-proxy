import os

import aiosmtpd.handlers
import aiosmtplib
import email
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.environ["SMTP_PORT"])
LOG_CONTENT = bool(os.environ.get("LOG_CONTENT", False))

class TransactionalHandler(aiosmtpd.handlers.AsyncMessage):
    async def handle_message(self, message: email.message.EmailMessage):
        transactional_mail = False
        if message.get("Remove-List-Unsubscribe", None):
            del message["List-Unsubscribe"]
            del message["Remove-List-Unsubscribe"]
            transactional_mail = True

        del message['X-Peer']
        del message['X-MailFrom']
        del message['X-RcptTo']

        await aiosmtplib.send(message, hostname=SMTP_HOST, port=SMTP_PORT)

        if transactional_mail:
            log.info(f'Transactional Mail has been sent to {",".join(message.get_all("to", []))}')
        else:
            log.info(f'Non-Transactional Mail has been sent to {",".join(message.get_all("to", []))}')

        if LOG_CONTENT:
            for part in message.walk():
                # each part is a either non-multipart, or another multipart message
                # that contains further parts... Message is organized like a tree
                if part.get_content_type() == 'text/plain':
                    log.info(part.get_payload())
                if part.get_content_type() == 'text/html':
                    log.info(part.get_payload())
