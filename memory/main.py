import argparse
import random
import sys
import time


class MemoryGame:
    def __init__(self):
        self.runs = 0
        self.right = 0
        self.wrongs = []

    def summary(self):
        print("Summary:")
        print(60 * "=")
        print(f"Runs: {self.runs}")
        print(f"Percentage: {(self.right / self.runs) * 100}%)")

    def increase_right(self):
        self.right += 1
        self.runs += 1

    def save_wrong(self, output, inp):
        self.wrongs.append({"output": output, "input": inp})
        self.runs += 1


def clear():
    sys.stdout.write("\033[2J\033[H")


def game_loop(interval, memory_func, game):
    ready = input("ready?")
    if ready == "quit" or ready == "exit":
        print("bye")
        exit(0)
    clear()
    output = memory_func()
    time.sleep(interval)
    clear()
    inp = input("enter the numbers:")
    if output != inp:
        print("wrong")
        print(output)
        print(30 * "=")
        print(inp)
        game.save_wrong(output, inp)
    else:
        print("right ✅")
        game.increase_right()


def parse_all_args():
    p = argparse.ArgumentParser()
    p.add_argument("-times", type=int, default=10)
    p.add_argument("-interval", type=int, default=2)
    p.add_argument("-num", type=int, default=4)
    return p.parse_args()


def memory(num):
    numbers = ""
    for _ in range(num):
        rand = random.randint(0, 100)
        numbers += str(rand) + ","
    print(numbers)
    return numbers[:-1]


def main():
    args = parse_all_args()
    print(args)
    game = MemoryGame()
    for _ in range(args.times):
        stop = game_loop(args.interval, lambda: memory(args.num), game)
        if stop:
            break
    game.summary()


if __name__ == "__main__":
    main()
