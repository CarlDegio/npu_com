import rclpy
from rclpy.node import Node
from npu_msg.msg import Direction,Pos
import serial
import struct
import _thread
import time
class MinimalSubscriber(Node):
	def __init__(self):
		super().__init__('minimal_subscriber')
		self.subscription = self.create_subscription(Direction,'com/move_direction',self.listener_callback,10)
		self.publisher=self.create_publisher(Pos,'com/q_pos',10)
		self.ser=serial.Serial('/dev/ttyACM0',115200,timeout=0.5) # 已经打开
		self.get_logger().info('open port')
		self.thread_end=False
		_thread.start_new_thread(self.publisher_callback,(1,))

	def listener_callback(self,msg):
		if(self.ser.isOpen() == True):
			self.get_logger().info(f'I heard lr: {msg.lr}')
			self.ser.write(self.msg_pack(msg))
		else:
			self.get_logger().info('port error')
    
	def msg_pack(self,msg):
		passage=struct.pack('fff',msg.lr,msg.ud,msg.fb)# bytes
		return passage
		
	def publisher_callback(self,delay):
		while True:
			if self.thread_end == True:
				_thread.exit()
			time.sleep(delay)#需要小于发布频率
			n=self.ser.inWaiting()
			if n:
				passage=self.ser.read(n)
				data=struct.unpack('fff',passage)
				pos=Pos()
				pos.q1=data[0]
				pos.q2=data[1]
				pos.q3=data[2]
				self.publisher.publish(pos)
				self.get_logger().info('Publishing: "%d"' % pos.q1)
	
	def __del__(self):
		self.ser.close()
		self.thread_end=True

def main(args=None):
	rclpy.init(args=args)
	minimal_subscriber = MinimalSubscriber()
	rclpy.spin(minimal_subscriber)
	minimal_subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
    main()
