import roslibpy

class RosbridgeClient:
    
    def __init__(self, host='localhost', port= 9090):
        self.host = host
        self.port = port

# Bağlantı durumu için event listener'lar
    def on_connection(self):
        print("Rosbridge sunucusuna bağlandı!")

    def on_error(self,error):
        print(f"Bağlantı hatası: {error}")

    def on_close(self):
        print("Rosbridge sunucusu bağlantısı kapandı.")
    
    def start(self):
        try:
            self.client = roslibpy.Ros(host=self.host, port=self.port)
            self.client.run()
            if self.client.is_connected:
                return True
            else:
                return False
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            return False

    def create_listener(self, topic_name, message_type,callback):
        listener= roslibpy.Topic(self.client, topic_name, message_type)
        listener.subscribe(callback)
    
        return listener

    def create_publisher(self, topic_name, message_type):
        publisher = roslibpy.Topic(self.client,topic_name,message_type)
        return publisher
    
    def terminate(self):
        self.client.terminate()

