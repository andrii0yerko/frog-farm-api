from geventwebsocket.exceptions import WebSocketError


class WSEndpoint():

    def __init__(self, blueprint, url):
        blueprint.add_url_rule(url, view_func=self.connect)

    def connect(self, client):
        modclient = self.on_connect(client)
        if modclient:
            client = modclient
        while not client.closed:
            message = client.receive()
            try:
                self.on_message(client, message)
            except WebSocketError:
                break
        self.on_disconnect(client)

    def on_connect(self, client):
        pass

    def on_message(self, client, message):
        pass

    def on_disconnect(self, client):
        pass
