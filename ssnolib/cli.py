import argparse
import pathlib
__this_dir__ = pathlib.Path(__file__).parent
def main():
    parser = argparse.ArgumentParser(
        description='ssnolib command line interface'
    )

    parser.add_argument('--h5sn',
                        help='Starts the streamlit app to semantically enrich hdf5 files with standard names',
                        action='store_true')
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
    if args.h5sn:
        import subprocess
        subprocess.run(
            ["streamlit", "run", str(__this_dir__ / "ui" / "h5snt" / "h5snt.py")],
            capture_output=True,
            text=True,
            check=True
        )
    if args.app:
        from ssnolib.ui.snt_manager import app
        app.app.run(debug=False, host=args.host, port=args.port)
