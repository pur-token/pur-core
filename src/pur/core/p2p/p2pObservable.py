from pur.core.notification.Observable import Observable
from pur.generated import purlegacy_pb2


class P2PObservable(Observable):
    def __init__(self, source):
        # FIpurE: Add mutexes
        super().__init__(source)

    def notify(self, message: purlegacy_pb2.LegacyMessage):
        # TODO: Add some p2p specific validation?
        super().notify(message)
