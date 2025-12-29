
import json
import time
import random

class StakeDiceBot:
    def __init__(self, strategy_path, initial_balance):
        self.strategy = self.load_strategy(strategy_path)
        self.base_balance = initial_balance
        self.current_balance = initial_balance
        self.bet_amount = self.calculate_base_bet()
        self.win_chance = 49.5
        self.wins = 0
        self.losses = 0
        self.total_games = 0
        self.profit = 0

    def load_strategy(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def calculate_base_bet(self):
        return (self.current_balance * self.strategy['base_bet_percent']) / 100

    def update_bet_and_chance(self):
        for condition in self.strategy['conditions']:
            trigger = condition['trigger']
            action = condition['action']
            if trigger == "every_loss" and self.losses > 0:
                self.bet_amount *= 1 + (action['percent'] / 100)
            elif trigger == "every_win" and self.wins > 0:
                self.win_chance -= action['percent']
            elif trigger == "every_2_losses" and self.losses % 2 == 0 and self.losses != 0:
                self.win_chance += action['percent']
            elif trigger == "win_streak_less_than" and self.wins < condition['value']:
                self.bet_amount *= 1 + (action['percent'] / 100)
            elif trigger == "win_streak_greater_than" and self.wins > condition['value']:
                self.bet_amount = self.calculate_base_bet()
            elif trigger == "loss_streak_greater_than" and self.losses > condition['value']:
                self.bet_amount = self.calculate_base_bet()
            elif trigger == "loss_streak_less_than" and self.losses < condition['value']:
                self.bet_amount *= 1 + (action['percent'] / 100)
            elif trigger == "every_200_games" and self.total_games % 200 == 0 and self.total_games != 0:
                self.bet_amount = self.calculate_base_bet()
                self.win_chance = 49.5

    def simulate_game(self):
        roll = random.uniform(0, 100)
        if roll <= self.win_chance:
            self.current_balance += self.bet_amount
            self.wins += 1
            self.losses = 0
        else:
            self.current_balance -= self.bet_amount
            self.losses += 1
            self.wins = 0
        self.profit = self.current_balance - self.base_balance
        self.total_games += 1

    def should_stop(self):
        gain_percent = (self.profit / self.base_balance) * 100
        return gain_percent >= self.strategy['session_cutoff']['percent_gain']

    def run(self):
        while not self.should_stop():
            self.simulate_game()
            self.update_bet_and_chance()
            print(f"Game {self.total_games}: Bet {self.bet_amount:.4f}, Chance {self.win_chance:.2f}%, Balance {self.current_balance:.4f}, Profit {self.profit:.4f}")
            time.sleep(0.1)

if __name__ == "__main__":
    bot = StakeDiceBot("stake_beast_bot_strategy.json", initial_balance=100)
    bot.run()
