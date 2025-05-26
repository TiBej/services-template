from common_lib.loggingfw import CustomLogFW

from flask import Flask, request, session, jsonify
import logging

logFW = CustomLogFW(service_name='user_service', instance_id='2')
handler = logFW.setup_logging()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

app = Flask(__name__)

@app.route('/trigger_log', methods=['GET'])
def bug():
    logging.info("bug is incoming")
    logging.critical("critical message")
    logging.error("Triggering bug...")
    return "Log triggered", 200

def main():
    app.run(host="0.0.0.0", port=5001)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
