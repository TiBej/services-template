import uuid


class BaseEvent:
    def __init__(self):
        self.correlation_id: uuid.UUID = uuid.uuid4()
