class AsymmetricExponentialSmoothing:
    def __init__(self):
        self.current_value = 0.0
        self.ease_in_progress = 0.0
        self.ease_out_progress = 0.0

    def ease_in(self, progress):
        # Quadratic ease in
        return progress ** 2

    def ease_out(self, progress):
        # Quadratic ease out
        return progress * (2 - progress)

    def smooth(self, new_value, alpha_rising, alpha_falling, ease_duration=1.0):
        if new_value > self.current_value:
            # When value is rising, use alpha_rising with ease in
            self.ease_in_progress = min(1.0, self.ease_in_progress + (1 / ease_duration))
            eased_alpha = alpha_rising * self.ease_in(self.ease_in_progress)
            self.current_value += eased_alpha * (new_value - self.current_value)
            self.ease_out_progress = 0.0  # Reset ease out progress
        else:
            # When value is falling, use alpha_falling with ease out
            self.ease_out_progress = min(1.0, self.ease_out_progress + (1 / ease_duration))
            eased_alpha = alpha_falling * self.ease_out(self.ease_out_progress)
            self.current_value += eased_alpha * (new_value - self.current_value)
            self.ease_in_progress = 0.0  # Reset ease in progress
        return self.current_value
