from enum import Enum

class RequestStatus(Enum):
    Accepted = 'Accepted'
    Rejected = 'Rejected'
    Sent = 'Sent'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)