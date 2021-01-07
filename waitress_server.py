from waitress import serve
import main as app 
serve(app.app, host='192.168.1.6', port=9000)