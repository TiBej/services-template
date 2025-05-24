# main_app.py

from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import requests
import logging
from loggingfw import CustomLogFW

app = Flask(__name__)

logFW = CustomLogFW(service_name='main_app', instance_id='1')
handler = logFW.setup_logging()
logging.getLogger().addHandler(handler)

@app.route('/')
def index():
    logging.info("Rendering index page...")
    return "hi"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
