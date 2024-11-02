#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32, Float32
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

class PWMPlotter:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('pwm_plotter', anonymous=True)

        # Parameters
        self.buffer_size = 100  # Number of data points to display

        # Data storage
        self.pwm_left_data = deque(maxlen=self.buffer_size)
        self.pwm_right_data = deque(maxlen=self.buffer_size)
        self.duty_cycle_left_data = deque(maxlen=self.buffer_size)
        self.duty_cycle_right_data = deque(maxlen=self.buffer_size)
        self.time_data = deque(maxlen=self.buffer_size)

        self.start_time = rospy.Time.now()

        # Subscribers
        rospy.Subscriber("/pwm_left", Int32, self.pwm_left_callback)
        rospy.Subscriber("/pwm_right", Int32, self.pwm_right_callback)
        rospy.Subscriber("/duty_cycle_left", Float32, self.duty_cycle_left_callback)
        rospy.Subscriber("/duty_cycle_right", Float32, self.duty_cycle_right_callback)

        # Setup Plot
        self.fig, (self.ax_pwm, self.ax_duty) = plt.subplots(2, 1, figsize=(10, 8))
        
        # PWM Plot
        self.line_pwm_left, = self.ax_pwm.plot([], [], label='PWM Left')
        self.line_pwm_right, = self.ax_pwm.plot([], [], label='PWM Right')
        self.ax_pwm.set_title('PWM Signals')
        self.ax_pwm.set_xlabel('Time (s)')
        self.ax_pwm.set_ylabel('PWM Value')
        self.ax_pwm.legend()
        self.ax_pwm.set_ylim(-300, 300)  # Adjust based on your PWM range

        # Duty Cycle Plot
        self.line_duty_left, = self.ax_duty.plot([], [], label='Duty Cycle Left')
        self.line_duty_right, = self.ax_duty.plot([], [], label='Duty Cycle Right')
        self.ax_duty.set_title('Duty Cycles')
        self.ax_duty.set_xlabel('Time (s)')
        self.ax_duty.set_ylabel('Duty Cycle (%)')
        self.ax_duty.legend()
        self.ax_duty.set_ylim(0, 100)

        # Animation
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update_plot,
            interval=100,  # Update every 100 ms
            blit=False
        )

    def pwm_left_callback(self, msg):
        current_time = (msg.header.stamp - self.start_time).to_sec() if msg.header.stamp else (rospy.Time.now() - self.start_time).to_sec()
        self.pwm_left_data.append(msg.data)
        self.time_data.append(current_time)

    def pwm_right_callback(self, msg):
        self.pwm_right_data.append(msg.data)
        # Assuming same timestamp as pwm_left
        if not self.time_data:
            current_time = (rospy.Time.now() - self.start_time).to_sec()
            self.time_data.append(current_time)

    def duty_cycle_left_callback(self, msg):
        self.duty_cycle_left_data.append(msg.data)

    def duty_cycle_right_callback(self, msg):
        self.duty_cycle_right_data.append(msg.data)
        # Assuming same timestamp as duty_cycle_left
        if not self.time_data:
            current_time = (rospy.Time.now() - self.start_time).to_sec()
            self.time_data.append(current_time)

    def update_plot(self, frame):
        # Update PWM plot
        times = list(range(-len(self.pwm_left_data)+1, 1))  # Simple time axis
        self.line_pwm_left.set_data(times, list(self.pwm_left_data))
        self.line_pwm_right.set_data(times, list(self.pwm_right_data))
        self.ax_pwm.set_xlim(-self.buffer_size, 0)

        # Update Duty Cycle plot
        self.line_duty_left.set_data(times, list(self.duty_cycle_left_data))
        self.line_duty_right.set_data(times, list(self.duty_cycle_right_data))
        self.ax_duty.set_xlim(-self.buffer_size, 0)

        return self.line_pwm_left, self.line_pwm_right, self.line_duty_left, self.line_duty_right

    def run(self):
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    try:
        plotter = PWMPlotter()
        plotter.run()
    except rospy.ROSInterruptException:
        pass
