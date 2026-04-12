from flask import Flask, request, jsonify, session
import pyotp
import qrcode
import io
import base64
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'vpn-demo-secret-key'
CORS(app)

# Demo user (for academic use)
USER = {
    'username': 'user',
    'password': 'pass',
    'totp_secret': pyotp.random_base32()
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == USER['username'] and data['password'] == USER['password']:
        session['username'] = data['username']
        return jsonify({'success': True, 'totp_required': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/totp-qr', methods=['GET'])
def totp_qr():
    # Generate QR code for Google Authenticator
    totp_uri = pyotp.totp.TOTP(USER['totp_secret']).provisioning_uri(name=USER['username'], issuer_name='VPN Demo')
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return jsonify({'qr': img_b64})

@app.route('/api/verify-totp', methods=['POST'])
def verify_totp():
    data = request.json
    totp = pyotp.TOTP(USER['totp_secret'])
    if totp.verify(data['code']):
        session['authenticated'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid TOTP code'})

if __name__ == '__main__':
    app.run(debug=True)
