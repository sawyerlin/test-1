#!/usr/bin/env python

import os

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import Dial, VoiceResponse
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

twilio_number = os.environ.get("TWILIO_CALLER_ID")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/token", methods=["GET"])
def token():
    # get credentials for environment variables
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    application_sid = os.environ["TWILIO_TWIML_APP_SID"]
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]

    number = request.args.get('number')

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=number)

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        outgoing_application_sid=application_sid,
        incoming_allow=True,
    )
    token.add_grant(voice_grant)

    # Return token info as JSON
    token = token.to_jwt()

    # Return token info as JSON
    return jsonify(identity=number, token=token)

@app.route('/voice', methods=['POST'])
def voice():
    resp = VoiceResponse()
    dial = Dial()
    dial.client(twilio_number)
    resp.append(dial)
    return Response(str(resp), mimetype="text/xml")

if __name__ == '__main__':
    app.run()
