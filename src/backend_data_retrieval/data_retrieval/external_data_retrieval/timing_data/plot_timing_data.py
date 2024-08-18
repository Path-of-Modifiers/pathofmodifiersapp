import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(filename):
    df = pd.read_csv(filename)

    time_diff = df["time_diff"].to_numpy()
    # max_time_diff = max(time_diff)

    # start_time = df.loc[1:, "start_time"].to_numpy()
    # n_data_points = len(start_time)
    # end_time = df.loc[: n_data_points - 1, "end_time"].to_numpy()

    # hand_off_time = abs(end_time - start_time)
    # max_hand_off_time = max(hand_off_time)

    # time_diff_divisible_by_10 = time_diff[: 10 * (len(time_diff) // 10)]
    # time_diff_wo_transformation = np.array(
    #     [
    #         time_diff_wo_transformation[10 * i : 10 * (i + 1) + 1]
    #         for i in range(len(time_diff_wo_transformation) // 10)
    #     ]
    # )
    # time_diff_wo_transformation = np.zeros(len(time_diff_divisible_by_10) - 9)
    # for i in range(len(time_diff_divisible_by_10) // 10):
    #     time_diff_wo_transformation += time_diff_divisible_by_10[10 * i : 10 * (i + 1)]

    # time_diff_wo_transformation = np.array(time_diff_wo_transformation)

    time_diff_wo_transformation = time_diff[np.where(time_diff >= 20)]

    n_requests_per_batch = 30
    time_per_request = time_diff_wo_transformation / n_requests_per_batch

    # plt.plot(time_diff / max_time_diff)
    plt.plot(time_per_request)
    plt.ylim((0, max(time_per_request) * 1.1))
    plt.xlim((0, len(time_per_request)))
    plt.title("Average time spent per request in a mini batch")
    plt.xlabel("Batch number [*]")
    plt.ylabel("Average time per request [s]")
    # plt.plot(hand_off_time / max_hand_off_time)
    # plt.ylim((0, max_hand_off_time))
    # plt.ylim((0, 1.1))
    # plt.show()


def main():
    plot("_process_stream/data.csv")
    # plot("_start_new_mini_expedition/loading_headers_first_1.csv")
    plt.show()
    return 0


if __name__ == "__main__":
    main()
