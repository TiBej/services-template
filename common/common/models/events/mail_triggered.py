class MailTriggeredEvent(BaseEvent):
    def __init__(self, recipient_email: str, subject: str, body: str):
        super().__init__()
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body