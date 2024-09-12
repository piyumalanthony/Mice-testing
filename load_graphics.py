import pandas as pd
import matplotlib.pyplot as plt
import copy
import seaborn as sns
import numpy as np
import sys
import argparse

if __name__ == '__main__':

    # if len(sys.argv) != 3:
    #     print("Usage: python example_sysargv.py <param1> <param2>")
    #     sys.exit(1)

    parser = argparse.ArgumentParser(description="Script that accepts multiple arguments")

    # Adding optional arguments
    parser.add_argument("-data", type=str, required=True, help="The csv file for loading data")
    parser.add_argument("-output", type=str, help="The output dir for save plots")
    parser.add_argument("-output2", type=str, help="The output dir for save plots of 5ms time gaps")

    args = parser.parse_args()

    file_path = args.data
    file_path_to_save = args.output
    file_path_to_save_2 = args.output2
    data = pd.read_csv(file_path, skiprows=16, header=0)

    data = data.reset_index(drop=True)
    data = data.drop(columns=data.columns[-1])
    data = data.drop(index=0)

    points = []
    elapsed_times = []
    loads = []

    elapsed_times_5ms = []
    loads_5ms = []
    displacement_5ms = []

    local_points = []
    local_elapsed_times = []
    local_loads = []

    local_elapsed_times_5ms = []
    local_loads_5ms = []
    local_displacement_5ms = []

    counter = 0
    displacement_counter = 0
    for index, row in data.iterrows():
        point_index = int(row["Points"])
        elapsed_time = float(row["Elapsed Time "])
        load = float(row["Load 1 "])
        displacement = float(row["Disp  "])
        local_points.append(point_index)
        local_elapsed_times.append(elapsed_time)
        local_loads.append(load)
        counter += 1
        displacement_counter += 1
        # print(counter)

        if 1<=point_index<=40 and counter < 100:
            local_elapsed_times_5ms.append(elapsed_time)
            local_loads_5ms.append(load)
            local_displacement_5ms.append(displacement)


        if counter == 500:
            points.append(copy.deepcopy(local_points))
            elapsed_times.append(copy.deepcopy(local_elapsed_times))
            loads.append(copy.deepcopy(local_loads))

            elapsed_times_5ms.append(copy.deepcopy(local_elapsed_times_5ms))
            loads_5ms.append(copy.deepcopy(local_loads_5ms))
            displacement_5ms.append(copy.deepcopy(local_displacement_5ms))

            local_points.clear()
            local_elapsed_times.clear()
            local_loads.clear()

            local_elapsed_times_5ms.clear()
            local_loads_5ms.clear()
            local_displacement_5ms.clear()

            counter = 0
            displacement_counter = 0

    for i in range(len(points)):
        points_data = points[i]
        elapsed_times_data = elapsed_times[i]
        loads_data = loads[i]
        plt.figure(figsize=(10, 6))
        plt.plot(elapsed_times_data, loads_data, marker='*')

        min_index = np.argmin(loads_data)
        max_value = np.max(loads_data)
        min_value = np.min(loads_data)
        load_range = max_value - min_value
        plt.plot(elapsed_times_data[min_index], loads_data[min_index], 'ro')
        plt.annotate(f'Min Value {loads_data[min_index]} at step {points_data[min_index]}',
                     xy=(elapsed_times_data[min_index], loads_data[min_index]),
                     xytext=(elapsed_times_data[min_index], loads_data[min_index] - load_range / 33), color='red',
                     ha='center')

        # Add titles and labels
        plt.title(f'Elapsed Time vs. Load 1 for cycle {i + 1}')
        plt.xlabel('Elapsed Time (Sec)')
        plt.ylabel('Load 1 (N)')

        # plt.xlim(min(elapsed_times_data)-0.5, max(elapsed_times_data) + 0.5)
        # plt.ylim(min(loads_data) - 0.005, max(loads_data) + 0.005)

        # Show the plots
        plt.grid(True)
        plt.savefig(f'{file_path_to_save}/cycle_{i + 1}.png')
        # plt.show()
        plt.clf()

        # Show the plots 5ms elapsed times gaps

        elapsed_times_data_5ms = elapsed_times_5ms[i]
        loads_data_5ms = loads_5ms[i]
        displacement_data_5ms = displacement_5ms[i]

        print(f'cycle {i + 1}')
        print(f'elapsed times: {elapsed_times_data_5ms}')
        print(len(elapsed_times_data_5ms))
        print(f'loads: {loads_data_5ms}')
        print(f'displacement: {displacement_data_5ms}')
        print('----------------------------------')
        # plt.figure(figsize=(10, 6))
        # plt.plot(elapsed_times_data_5ms, loads_data_5ms, marker='*', color='red')
        # plt.plot(elapsed_times_data_5ms, displacement_data_5ms, marker='.', color='green')
        # plt.title(f'Elapsed Time vs. Load 1/Displacement for cycle {i + 1}')
        # plt.xlabel('Elapsed Time (Sec)')
        # plt.ylabel('Load 1 (N)/Displacement (mm)')
        # plt.grid(True)
        # plt.savefig(f'{file_path_to_save_2}/cycle_{i + 1}.png')
        # # plt.show()
        # plt.clf()

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot data for the first y-axis
        ax1.plot(elapsed_times_data_5ms, loads_data_5ms, marker='*', color='red', label='Load 1 data')
        ax1.set_xlabel('Elapsed_time (s)')
        ax1.set_ylabel('Load 1 (N)', color='red')
        # ax1.tick_params(axis='y', labelcolor='b')

        # Create the second y-axis using twinx
        ax2 = ax1.twinx()
        ax2.plot(elapsed_times_data_5ms, displacement_data_5ms, marker='.', color='green', label='Displacement data')
        ax2.set_ylabel('Displacement (mm)', color='green')
        # ax2.tick_params(axis='y', labelcolor='r')

        # Add legends for both axes
        ax1.legend(loc='upper left', bbox_to_anchor=(0, 1), borderaxespad=0.)
        ax2.legend(loc='upper right', bbox_to_anchor=(1, 1), borderaxespad=0.)

        # Automatically adjust the layout
        fig.tight_layout()
        plt.title(f'Elapsed Time vs. Load 1/Displacement for cycle {i + 1}')

        plt.grid(True)
        plt.savefig(f'{file_path_to_save_2}/cycle_{i + 1}.png')
        # plt.show()
        plt.clf()

