class AsymmetricExponentialSmoothing:
    def __init__(self, low_threshold=12, delay_limit=20):
        """
        Initialize the smoothing factors and delay mechanism.
        :param low_threshold: The threshold below which the delay mechanism activates.
        :param delay_limit: The number of iterations to delay the rising process.
        """
        self.current_value = 0.0
        self.low_threshold = low_threshold
        self.delay_limit = delay_limit
        self.delay_counter = 0

    def smooth(self, new_value, alpha_rising, alpha_falling):
        """
        Apply the smoothing logic based on the direction of the value change, with delay for low values.
        :param new_value: The new sensor value.
        :return: Smoothed value.
        """
        if new_value > self.current_value:
            # When value is rising, check if delay is needed
            if self.current_value < self.low_threshold and self.delay_counter < self.delay_limit:
                print("keep it!!")
                # Increment delay counter and keep current value
                self.delay_counter += 1
            else:
                # Reset delay counter and apply rising smoothing
                self.delay_counter = 0
                self.current_value += alpha_rising * (new_value - self.current_value)
        else:
            # When value is falling, use alpha_falling and reset delay counter
            self.delay_counter = 0
            self.current_value += alpha_falling * (new_value - self.current_value)
        return self.current_value

# Example usage
# sensor_data_processor = AsymmetricExponentialSmoothing(low_threshold=0.1, delay_limit=5)

# In your loop, you would use it like this:
# sensor_value = get_sensor_value()  # replace this with actual sensor data fetching
# smoothed_value = sensor_data_processor.smooth(sensor_value, alpha_rising=0.8, alpha_falling=0.2)
