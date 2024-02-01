import threading
import requests 
from datetime import datetime

class WebController:
    baseurl = "http://llum.htmlfiesta.com/api.php"
    skiptimes=1000
    skipcounter={}

    def __init__(self):
        pass

    @staticmethod
    def updatesensor(id,  batterylevel):
        shouldsend=False
        if id in WebController.skipcounter:
            WebController.skipcounter[id]-=1
            if WebController.skipcounter[id]==0:
                #reset
                shouldsend=True
                WebController.skipcounter[id]=WebController.skiptimes
        else:
            WebController.skipcounter[id]=WebController.skiptimes
            shouldsend=True

        if shouldsend:
            now_time = datetime.now().strftime("%H_%M_%S")
            # Construct the final URL with query parameters
            final_url = f"{WebController.baseurl}?sensor={id}&lastupdate={now_time}&battery={batterylevel}"
            # Start a thread to send the request without blocking
            thread = threading.Thread(target=WebController._send_request, args=(final_url,))
            thread.start()

    @staticmethod
    def _send_request(url):
        try:
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                pass
                #print(f"Success: {response.text}")
            else:
                print(f"Error: Received response code {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Handle requests exceptions (e.g., connection errors)
            print(f"Request failed: {e}")

"""
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
"""