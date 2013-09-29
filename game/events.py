from django_socketio.events import Namespace
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace


GAME_STATES = {
    "AVAILABLE": 1,
    "INGAME": 2,
    "WAITING": 3,
}

@Namespace('/users')
class UserNamespace(BaseNamespace, BroadcastMixin):
    users = []

    def on_join(self, user):
        user['gamestate']  = GAME_STATES['AVAILABLE']
        self.users.append(user)
        self.emit('join', self.users)
        self.broadcast_event_not_me('connected', user)



