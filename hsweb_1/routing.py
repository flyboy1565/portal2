from channels.routing import route
from accounts.consumers import ws_connect, ws_disconnect
from issues.consumers import ws_notify_issue


channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
    route('websocket.issues', ws_notify_issue),
]