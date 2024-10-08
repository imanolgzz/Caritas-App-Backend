from flask import request
from os import getenv
from secure import Secure
import ssl

from routes import initialize_app

app = initialize_app()
secure_headers = Secure.with_default_headers()

@app.after_request
def add_security_headers(r):
    secure_headers.set_headers(r)
    #r.headers['X-Frame-Options'] = 'SAMEORIGIN' # ya lo llena 'secure'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #r.headers["Expires"] = "0"

    if 'apidocs' in request.url:
        r.headers["Content-Security-Policy"] = ""
    
    return r

if __name__ == '__main__':
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain(getenv("API_CERT_PROD"), getenv("API_KEY_PROD"))
	app.run(host=getenv("API_HOST_PROD"), port = getenv("API_PORT_PROD"), ssl_context=context,debug=True)
