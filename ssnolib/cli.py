import argparse


def main():
    parser = argparse.ArgumentParser(
        description='ssnolib command line interface'
    )

    parser.add_argument('--app',
                        help='Starts the flask web app',
                        action='store_true')
    parser.add_argument('-p', '--port',
                        help='Port to run the server on',
                        type=int,
                        default=5000)
    parser.add_argument('-H', '--host',
                        help='Host to run the server on',
                        type=str,
                        default='127.0.0.1')
    args = parser.parse_args()

    if args.app:
        from ssnolib.ui import app
        app.app.run(debug=False, host=args.host, port=args.port)
