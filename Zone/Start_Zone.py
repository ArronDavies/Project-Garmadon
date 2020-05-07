from Zone.ZoneServer import ZoneServer
import configparser
import asyncio
import flask
import threading
import sys

config = configparser.ConfigParser()
config.read('../config.ini')
zone_info = config['ZONE']


def flask_thread():
    app = flask.Flask(__name__)
    app.static_folder = 'static'
    app.config["DEBUG"] = False
    app.use_reloader = False

    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

    @app.route('/kick_player/<UUID>', methods=['GET'])
    def kick_player(UUID):
        zone.kick_player(UUID=UUID)

    app.run(host=zone_info['Bindip'], port=11100)


if __name__ == "__main__":
    zone = ZoneServer("1100", 1100)  # id, port

    api = threading.Thread(target=flask_thread)
    api.start()
    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
