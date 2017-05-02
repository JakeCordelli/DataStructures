
from watson_developer_cloud import SpeechToTextV1
import json

stt = SpeechToTextV1(username="790fcd0d-6fb4-4fe3-9049-5fdefa01667c", password="1FQ5kdMYPgBu")
audio_file = open("/Users/JakeCordelli/Desktop/test2.wav", "rb")

print ((json.dumps(stt.recognize(audio_file, content_type="audio/wav"), indent=2)))

from ws4py.client.threadedclient import WebSocketClient
import base64, json, ssl, subprocess, threading, time

class SpeechToTextClient(WebSocketClient):
    def __init__(self) -> object:
        """

        :rtype: object
        """
        ws_url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize"

        username = "790fcd0d-6fb4-4fe3-9049-5fdefa01667c"
        password = "1FQ5kdMYPgBu"
        auth_string = "%s:%s" % (username, password)
        base64string = base64.encodestring(auth_string).replace("\n", "")

        self.listening = False

        try:
            WebSocketClient.__init__(self, ws_url,
                headers=[("Authorization", "Basic %s" % base64string)])
            self.connect()
        except: print ("Failed to open WebSocket.")

    def opened(self):
        self.send('{"action": "start", "content-type": "audio/l16;rate=16000"}')
        self.stream_audio_thread = threading.Thread(target=self.stream_audio)
        self.stream_audio_thread.start()

    def received_message(self, message):
        message = json.loads(str(message))
        if "state" in message:
            if message["state"] == "listening":
                self.listening = True
        print ("Message received: " + str(message))

    def stream_audio(self):
        while not self.listening:
            time.sleep(0.1)

        reccmd = ["arecord", "-f", "S16_LE", "-r", "16000", "-t", "raw"]
        p = subprocess.Popen(reccmd, stdout=subprocess.PIPE)

        while self.listening:
            data = p.stdout.read(1024)

            try: self.send(bytearray(data), binary=True)
            except ssl.SSLError: pass

        p.kill()

    def close(self):
        self.listening = False
        self.stream_audio_thread.join()
        WebSocketClient.close(self)

try:
    stt_client = SpeechToTextClient()
    #raw_input()
finally:
    stt_client.close()