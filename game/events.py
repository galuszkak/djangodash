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
        user['gamestate'] = GAME_STATES['AVAILABLE']
        if any(filter(lambda u: u['username'] == user['username'], self.users)):
            self.error("user_connected", "User is connected")     
        else:
            self.users.append(user)
            self.broadcast_event_not_me('connected', user)
        
        self.emit('join', self.users)
        

    def recv_disconnect(self):
        # Remove nickname from the list.
        # TODO
        # self.log('Disconnected')
        # nickname = self.socket.session['nickname']
        # self.nicknames.remove(nickname)
        # self.broadcast_event('announcement', '%s has disconnected' % nickname)
        # self.broadcast_event('nicknames', self.nicknames)
        # self.disconnect(silent=True)
        # return True
        pass