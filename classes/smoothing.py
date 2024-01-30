class AsymmetricExponentialSmoothing:
    def __init__(self):
        """
        Initialize the smoothing factors.
        :param alpha_rising: Smoothing factor for rising edge (0.0 to 1.0).
        :param alpha_falling: Smoothing factor for falling edge (1.0 to 0.0).
        """
        #self.alpha_rising = alpha_rising
        #self.alpha_falling = alpha_falling
        self.current_value = 0.0

    def smooth(self, new_value,alpha_rising,alpha_falling):
        """
        Apply the smoothing logic based on the direction of the value change.
        :param new_value: The new sensor value.
        :return: Smoothed value.
        """
        if new_value > self.current_value:
            # When value is rising, use alpha_rising
            self.current_value += alpha_rising * (new_value - self.current_value)
        else:
            # When value is falling, use alpha_falling
            self.current_value += alpha_falling * (new_value - self.current_value)
        return self.current_value

# Example usage
#sensor_data_processor = AsymmetricExponentialSmoothing(alpha_rising=0.8, alpha_falling=0.2)

# In your loop, you would use it like this:
# sensor_value = get_sensor_value()  # replace this with actual sensor data fetching
# smoothed_value = sensor_data_processor.smooth(sensor_value)
