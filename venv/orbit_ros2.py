import roslibpy

class RosbridgeClient:
    
    def __init__(self, host='localhost', port= 9090):
        
        self.client = roslibpy.Ros(host='localhost', port=9090)
        self.client.on('connection', self.on_connection)
        self.client.on('error', self.on_error)
        self.client.on('close', self.on_close)

# Bağlantı durumu için event listener'lar
    def on_connection(self):
        print("Rosbridge sunucusuna bağlandı!")

    def on_error(self,error):
        print(f"Bağlantı hatası: {error}")

    def on_close(self):
        print("Rosbridge sunucusu bağlantısı kapandı.")
    
    def start(self):
        try:
            self.client.run_forever()
        except KeyboardInterrupt:
            print("Bağlantı kapatılıyor...")
            self.client.terminate()

    def create_listener(self, topic_name, message_type,callback):
        listener= roslibpy.Topic(self.client, topic_name, message_type)
        listener.subscribe(callback)
    
        return listener

    def create_publisher(self, topic_name, message_type):
        publisher = roslibpy.Topic(self.client,topic_name,message_type)
        return publisher

