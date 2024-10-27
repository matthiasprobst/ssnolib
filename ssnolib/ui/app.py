import json
from dataclasses import dataclass

from flask import Flask, render_template, request, redirect

import ssnolib
from ssnolib.ui.utils import fetch_form_data, snt_to_cache_data

app = Flask(__name__)

cache = {
    "data": {},
    "warning_messages": {},
    "error_messages": {}
}


@dataclass
class WarningMessage:
    category: str
    message: str


@app.route('/')
def welcome():
    return render_template('welcome/index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('core/index.html', data={})


@app.route('/JSON-LD', methods=['POST'])
def json_ld():
    json_data, data, warning_messages, error_messages, has_errors = fetch_form_data(request, cache["warning_messages"])
    cache["data"] = data.copy()
    cache["warning_messages"] = warning_messages.copy()
    cache["error_messages"] = error_messages
    return render_template(
        'post/jsonld.html',
        json_data=json_data,
        error_messages=error_messages.messages if has_errors else None
    )


@app.route('/reload', methods=['GET'])
def reload():
    has_warnings = False
    for k, v in cache["warning_messages"].items():
        if len(v) > 0:
            has_warnings = True
            break
    return render_template(
        'core/index.html',
        data=cache["data"],
        warning_messages=cache["warning_messages"] if has_warnings else None)


@app.route('/load', methods=['POST'])
def load():
    # Get the uploaded file
    json_content = json.load(request.files['jsonld_file'])
    warning_messages = {"UnitParsWarnings": []}
    try:
        snt = ssnolib.parse_table(data=json_content)

        data, warning_messages = snt_to_cache_data(snt, warning_messages)

        has_warnings = False
        for k, v in warning_messages.items():
            if len(v) > 0:
                has_warnings = True
                break

        cache["data"] = data.copy()
        cache["warning_messages"] = warning_messages.copy()

        # Render the form with pre-filled data
        return render_template('core/index.html', data=data,
                               warning_messages=warning_messages if has_warnings else None)
    except Exception as e:
        pass
    # Redirect back to the welcome page if the file is not valid
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
