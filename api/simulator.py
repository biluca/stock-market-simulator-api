import random

VOLATILITY = 3
SPEED_OF_MEAN_REVERSION = 0.01

RANDOM_MEAN_FLOOR = random.uniform(20, 30)
RANDOM_MEAN_SEILING = random.uniform(80, 100)

RANDOM_NOISE_FLOOR = random.uniform(-1, -0.1)
RANDOM_NOISE_SEILING = random.uniform(0.1, 1)


class MeanReversionSimulator:
    def generate_next_price(self):
        self.mean_price = random.uniform(RANDOM_MEAN_FLOOR, RANDOM_MEAN_SEILING)
        self.speed_of_mean_reversion = SPEED_OF_MEAN_REVERSION
        self.current_price = self.mean_price

        diff_from_mean = self.mean_price - self.current_price
        price_change = (
            self.speed_of_mean_reversion * diff_from_mean
            + random.uniform(RANDOM_NOISE_FLOOR, RANDOM_NOISE_SEILING) * VOLATILITY
        )
        self.current_price += price_change

        if self.current_price < 0:
            return 0

        return self.current_price
