"""
Coordination des synchronisations : empeche deux synchronisations
simultanees et memorise le resultat de la derniere.

Volontairement independant de FastAPI : la traduction de
SyncAlreadyRunning en reponse HTTP 409 est faite dans routes/sync.py,
la couche qui connait le protocole HTTP.
"""

from threading import Lock


class SyncAlreadyRunning(Exception):
    pass


class SyncCoordinator:

    def __init__(self, pipeline):

        self.pipeline = pipeline
        self.last_sync = None
        self._lock = Lock()

    def run(self) -> dict:

        if not self._lock.acquire(blocking=False):
            raise SyncAlreadyRunning()

        try:
            self.last_sync = self.pipeline.run_sync()
            return self.last_sync
        finally:
            self._lock.release()
