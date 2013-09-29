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
    logged_in = {}

    def on_join(self, user):
        #import ipdb; ipdb.set_trace();
        print "OnJoin SessionId " + self.socket.sessid
        user['gamestate'] = GAME_STATES['AVAILABLE']
        if any(filter(lambda u: u['username'] == user['username'], self.users)):
            self.error("user_connected", "User is connected")     
            self.logged_in[user['username']] = self.socket.sessid
        else:
            self.logged_in[user['username']] = self.socket.sessid
            self.users.append(user)
            print 'JOIN ' + user['username']
            self.broadcast_event_not_me('connected', user)
        print self.users
        self.emit('join', self.users)
        

    def recv_disconnect(self):
        user_list = filter(lambda (user, sessid):sessid==self.socket.sessid, self.logged_in.items())

        if any(user_list):            
            self.logged_in.pop(user_list[0][0])
            user = [user for user in self.users if user['username'] == user_list[0][0]][0]
            self.users.remove(user)
            self.broadcast_event_not_me('left', user)
        return True
    
    
