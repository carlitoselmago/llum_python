from flask import Flask, redirect, url_for, request

class WebController:

    ip="0.0.0.0"
    port=8080

    def __init__(self,OSXDMX=False):
       
        self.OSXDMX=OSXDMX
        
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home', self.home)
    
    def home(self):
        html = '<h4>SOFIA LLUM</h4>'
        if self.OSXDMX:
            html += '<p>SECONDS TO END: <b>' + str(self.OSXDMX.secondsleft) + '</b></p>'
        html += '<script>setTimeout(function () { location.reload(1); }, 5000);</script>'
        return html

    def run(self):
        self.app.run(host=self.ip,port=self.port,debug=True,use_reloader=False)

if __name__ == '__main__':
    web_controller = WebController()
    web_controller.run()