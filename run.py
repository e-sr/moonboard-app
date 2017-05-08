from moonBoardApp import app,socket
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run moonboard app')
    parser.add_argument('--debug',  action="store_true", default=False, help='Debug modus')
    parser.add_argument('--host', action="store", default='127.0.0.1', help='Host addressw')
    parser.add_argument('--port',  type=int, default=5000, help='Server port')
    args = parser.parse_args()

    socket.run(app, host=args.host, port=args.port,debug=args.debug)