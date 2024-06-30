import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot(filename):
    df = pd.read_csv(filename)

    time_diff = df["time_diff"].to_numpy()
    max_time_diff = max(time_diff)

    start_time = df.loc[1:, "start_time"].to_numpy()
    n_data_points = len(start_time)
    end_time = df.loc[: n_data_points - 1, "end_time"].to_numpy()

    hand_off_time = abs(end_time - start_time)
    max_hand_off_time = max(hand_off_time)

    plt.plot(time_diff / max_time_diff)
    # plt.ylim((0, max_time_diff))
    plt.plot(hand_off_time / max_hand_off_time)
    # plt.ylim((0, max_hand_off_time))
    plt.ylim((0, 1.1))
    plt.show()


def main():
    plot("_start_new_mini_expedition/0.csv")
    return 0


if __name__ == "__main__":
    main()
