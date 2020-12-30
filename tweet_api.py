import os
from flask import Flask, stream_with_context, request, Response
app = Flask(__name__)


def run_flask():
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'  # Suppress startup messages in stdout
    app.run()


@app.route('/tweets')
def streamed_response():
    @stream_with_context
    def generate():
        yield "test"
        yield " "
        yield request.args.get("user", "No user specified")
    return Response(generate())

