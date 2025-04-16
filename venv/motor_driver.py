from orbit_ros2 import RosbridgeClient
import time
from math import atan2, sin, cos
import math 
import roslibpy

class Controller:
    def __init__(self,host= 'localhost',port=9090):
        self.ros_client = RosbridgeClient(host= 'localhost',port=9090)
        self.max_speed = 1.0
        self.current_position= None
        

    def move_forward(self,speed:float):
        """ Robot burada ileri gidecek """
        

        publisher =self.ros_client.create_publisher(topic_name='/cmd_vel', message_type='geometry_msgs/Twist')
        if speed < 0.0 or speed > self.max_speed:
            raise Exception(f"Hızın değeri aralık dışındadır: [0.0, {self.max_speed}]")
     
        message = {
            'linear' : {'x' : speed, 'y' : 0.0, 'z': 0.0},
            'angular' : {'x' : 0.0, 'y': 0.0, 'z': 0.0}
        }
        publisher.publish(message)
        print(f"/cmd_vel üzerinden mesaj yayınlandı: Linear X = {message['linear']['x']}, Angular Z = {message['angular']['z']}")
        self.ros_client.start()
            
        
    
    def move_backward(self,speed:float):
        """ Robot burada geriye gidecek.  """

        publisher =self.ros_client.create_publisher(topic_name='/cmd_vel', message_type='geometry_msgs/Twist')
        if speed < 0.0 or speed > self.max_speed:
            raise Exception(f"Hızın değeri aralık dışındadır: [{-self.max_speed},0.0]")
     
        message = {
            'linear' : {'x' : -speed, 'y' : 0.0, 'z': 0.0},
            'angular' : {'x' : 0.0, 'y': 0.0, 'z': 0.0}
            
        }
        
        publisher.publish(message)
        print(f"/cmd_vel üzerinden mesaj yayınlandı: Linear X = {message['linear']['x']}, Angular Z = {message['angular']['z']}")
        self.ros_client.start()
            
      
    def stop_the_car(self):
        """ Robot burada duracak."""

        publisher =self.ros_client.create_publisher(topic_name='/cmd_vel', message_type='geometry_msgs/Twist')
        
     
        message = {
            'linear' : {'x' : 0.0, 'y' : 0.0, 'z': 0.0},
            'angular' : {'x' : 0.0, 'y': 0.0, 'z': 0.0}
            
        }
        
        publisher.publish(message)
        print(f"/cmd_vel üzerinden mesaj yayınlandı: Linear X = {message['linear']['x']}, Angular Z = {message['angular']['z']}")
    
        self.ros_client.start()

    def turn_right(self):
        """Robot burada 90 derece dönüş yapacak"""
        

        publisher = self.ros_client.create_publisher(topic_name= '/cmd_vel',message_type='geometry_msgs/Twist')
        
        message = {
            'linear' : {'x' : 0.0, 'y' : 0.0, 'z': 0.0},
            'angular' : {'x' : 0.0, 'y': 0.0, 'z': -1.57}
        }
    
        publisher.publish(message)
        print(f"/cmd_vel üzerinden mesaj yayınlandı: Linear X = {message['linear']['x']}, Angular Z = {message['angular']['z']}")
        self.ros_client.start()

    def turn_left(self):
        """"Robot burada sola dönecek"""
        
        publisher = self.ros_client.create_publisher(topic_name='/cmd_vel', message_type='geometry_msgs/Twist')
        
        message = {
            'linear' : {'x': 0.0, 'y': 0.0, 'z': 0.0},
            'angular' : {'x': 0.0, 'y': 0.0, 'z': 1.57}
        }
        publisher.publish(message)
        print(f"/cmd_vel üzerinden mesaj yayınlandı: Linear X = {message['linear']}")
        
        self.ros_client.start()

    def get_distance(self,pos1,pos2):
        return math.sqrt((pos1['x']- pos2['x'])**2 + (pos1['y']-pos2['y'])**2)
    
    
    def update_position(self, message):
        """ Callback function to update the current position from /odom topic """
        if 'pose' in message and 'pose' in message['pose']:  
            position = message['pose']['pose']['position']
            self.current_position = {'x': position['x'], 'y': position['y']}

    

    def move_forward_steps(self,distance):
        """Robot burada girilen mesafe kadar hareket edecek."""

        self.publisher_ = self.ros_client.create_publisher(topic_name='/move_forward_topic',message_type='/std_msgs/msg/Float32')
        
        forward_msg = {'data' : distance}
        self.publisher_.publish(forward_msg)
        print("distance gönderildi.")
       
        
        self.ros_client.start()
        
    def move_backward_steps(self,distance_b):
        """Robot burada girilen mesafe kadar hareket edecek."""
  
        vel_pub = self.ros_client.create_publisher(topic_name='/move_backward_topic',message_type='/std_msgs/msg/Float32')
        backward_msg = {'data' : distance_b}
        vel_pub.publish(backward_msg)
        print("backward distance gönderildi.")
        self.ros_client.start()
        
    
    def get_position(self):
        self.ros_client
        def callback_tf(message):
            self.current_position= {}
            if 'transforms' in message:
                transforms = message['transforms']
                for transform in transforms:
                    if 'header' in transform and 'transform' in transform:
                        frame_id = transform['header']['frame_id']
                        child_frame_id = transform['child_frame_id']
                        if frame_id == 'odom' and child_frame_id == 'base_footprint':
                            translation = transform['transform']['translation']
                            rotation = transform['transform']['rotation']
                            self.current_position = {
                                'translation' :{
                                    'x' : translation['x'],
                                    'y' : translation['y'],
                                    'z' : translation['z']
                                },
                                'rotation' : {
                                    'x' :rotation['x'],
                                    'y' :rotation['y'],
                                    'z' :rotation['z'],
                                    'w' :rotation['w']
                                    
                                }
                            }
                            #print(f"Robot Konumu:\n  translation: \n  x={self.current_position['translation [x]']},\n y={self.current_position['translation [y]']},\n z={self.current_position['translation [z]']},\n rotation: \n   x={self.current_position['rotation [x]']},\n y={self.current_position['rotation [y]']},\n  z={current_position['rotation [z]']},\n  w={self.current_position['rotation [w]']} ")
            
                        #else :
                            #print("Hata frame_id: map bulunamadı")
                    else: 
                        print("Hata : 'transform' alanı bulunamadı! ")
            else:
                print("Hata: 'transforms' alanı bulunamadı")
            self.publish_position()
            return self.current_position

        subscriber = self.ros_client.create_listener(topic_name='tf', message_type='tf2_msgs/TFMessage',callback=callback_tf)
        self.ros_client.start()
    def publish_position(self):
            if self.current_position is not None:
                try:
                    # Create a proper message to publish
                    position_msg = {
                        'data': [
                            self.current_position['translation']['x'],
                            self.current_position['translation']['y'],
                            self.current_position['translation']['z'],
                            self.current_position['rotation']['x'],
                            self.current_position['rotation']['y'],
                            self.current_position['rotation']['z'],
                            self.current_position['rotation']['w']
                        ]
                    }
                    self.position_publisher = self.ros_client.create_publisher(topic_name='/tf_topic', message_type='tf2_msgs/TFMessage')
                    self.position_publisher.publish(position_msg)
                except Exception as e:
                    pass 
    def turn_right_position(self,speed, use_degree=False):
        "Hız değerini radyan olarak [0.0, 6.28] aralığında; hız değerini derece olarak [0,360] derece aralığında girin."
             
        if use_degree:
            speed = (math.pi/180)*speed
            print(f'speed : {speed}')
        else:
            if speed< 0.0 or speed> 6.28:
                raise Exception("Hız değeri : Out of range ")
     
        self.publish_message(-speed)
    
        self.ros_client.start()
    def turn_left_position(self,speed, use_degree = False):
        "Hız değerini radyan olarak [0.0, 6.28] aralığında; hız değerini derece olarak [0,360] derece aralığında girin."
             
        if use_degree:
            speed = (math.pi/180)*speed
            print(f'speed : {speed}')
        else:
            if speed< 0.0 or speed> 6.28:
                raise Exception("Hız değeri : Out of range ")
     
        self.publish_message(speed)
        self.ros_client.start()
    
    
    def reset_position(self):
        publisher_request=self.ros_client.create_publisher(topic_name='/reset_request',message_type='std_msgs/msg/Float32')
        
        reset_msg = {'data': 5}

        publisher_request.publish(reset_msg)
        print("mesaj alındı mı")
        self.ros_client.start()     
    

    def publish_message(self,angular_speed):
        publisher = self.ros_client.create_publisher(topic_name='/angular_speed',message_type='std_msgs/msg/Float32')
           
        message = {'data': angular_speed}
     
        publisher.publish(message)
        print('mesaj yayınlandı')
        self.ros_client.start()


    def get_temperature(self):
        
        self.publisher_temp =self.ros_client.create_publisher(topic_name='get_temp_func',message_type='std_msgs/msg/Float32')
        
        temp_msg = { 'data': 20}
        def callback_temp(msg):
            temp=msg['data']
            print("Oda sıcaklığı :{:.2f} ".format(temp))
            
        self.publisher_temp.publish(temp_msg)
        
        self.ros_client.create_listener(topic_name='/get_temp', message_type = 'std_msgs/msg/Float32',callback=callback_temp)

        self.ros_client.start()

            
    