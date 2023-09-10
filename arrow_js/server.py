#https://github.com/amoeba/arrow-python-js-ipc-example/blob/main/server/server.py
from io import BytesIO

from flask import Flask, render_template, send_file
from flask_cors import CORS
import pyarrow as pa

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
   return render_template('index.html')

@app.get("/d.arrow")
def get_arrow():
    data = [
        pa.array(['A', 'B', 'C', 'D']),
        pa.array([28, 55, 43, 91], type=pa.int32())
    ]

    batch = pa.record_batch(data, names=['category', 'amount'])

    sink = pa.BufferOutputStream()

    with pa.ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)

    return send_file(BytesIO(sink.getvalue().to_pybytes()), "data.arrow")