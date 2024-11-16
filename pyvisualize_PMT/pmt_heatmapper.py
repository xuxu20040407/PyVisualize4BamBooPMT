import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


class BottomPMTHeatmapper:
    def __init__(self, dis_bot,folder_path,new_folder):
        self.folder_path = folder_path
        self.dis_bot = dis_bot
        self.new_folder = new_folder

    def process_file(self, filename):
        file_path = os.path.join(self.folder_path, filename)
        coords = np.load(file_path)
        print(coords.shape)

        third_row = coords[2, :]
        bool_index = third_row < 0
        pmt_number = coords[3, bool_index]

        x_coords, y_coords = [], []
        for i in range(-50, 50):
            for j in range(-50, 50):
                x0 = i * self.dis_bot if j % 2 == 0 else i * self.dis_bot + self.dis_bot * 0.5
                y0 = (j * self.dis_bot) * np.sqrt(3) * 0.5
                x = i * self.dis_bot
                y = j * self.dis_bot
                if x0 * x0 + y0 * y0 < 945.0 * 945.0:
                    x_coords.append(x)
                    y_coords.append(y)
        coordinates = list(zip(x_coords, y_coords))

        n_values, n_counts = np.unique(pmt_number, return_counts=True)
        all_pmt_numbers = np.arange(2304, 2803)
        count_dict = {pmt_num: 0 for pmt_num in all_pmt_numbers}
        for value, count in zip(n_values, n_counts):
            count_dict[value] = count

        n_counts = np.array(list(count_dict.values()))

        df = pd.DataFrame(list(zip(x_coords, y_coords)), columns=['X', 'Y'])
        unique_x = sorted(df['X'].unique())
        unique_y = sorted(df['Y'].unique())

        freq_matrix = np.zeros((len(unique_y), len(unique_x)))
        for idx, (x, y) in enumerate(coordinates):
            ix = unique_x.index(x)
            iy = unique_y.index(y)
            freq_matrix[iy, ix] = n_counts[idx]

        freq_df = pd.DataFrame(freq_matrix, index=unique_y, columns=unique_x)

        if freq_df.empty:
            print(f"Frequency DataFrame is empty for {filename}.")
            return

        plt.figure(figsize=(10, 8))
        sns.heatmap(freq_df, cmap='viridis', fmt=".0f", linewidths=.5, square=True)
        plt.title(f'PMT Heatmap - {filename}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')

        image_path = os.path.join(self.new_folder, f'{filename[:-4]}.png')
        plt.savefig(image_path)
        plt.close()

    def process_all_files(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.npy'):
                self.process_file(filename)



class TopPMTHeatmapper:
    def __init__(self, dis_top,folder_path,new_folder):
        self.folder_path = folder_path
        self.dis_top = dis_top
        self.new_folder = new_folder

    def process_file(self, filename):
        file_path = os.path.join(self.folder_path, filename)
        coords = np.load(file_path)
        print(coords.shape)

        third_row = coords[2, :]
        bool_index = third_row > 0
        pmt_number = coords[3, bool_index]

        pmtx, pmty = [], []
        x_coords, y_coords = [], []
        for i in range(100):
            for j in range(100):
                x = -50 * self.dis_top + self.dis_top / 2 + i * self.dis_top
                y = -50 * self.dis_top + self.dis_top / 2 + j * self.dis_top
                if x * x + y * y < 960 * 960:
                    pmtx.append(x)
                    pmty.append(y)

                    x_coords.append(x - 12.125)
                    y_coords.append(y + 12.125)

                    x_coords.append(x + 12.125)
                    y_coords.append(y + 12.125)

                    x_coords.append(x - 12.125)
                    y_coords.append(y - 12.125)

                    x_coords.append(x + 12.125)
                    y_coords.append(y - 12.125)
        coordinates = list(zip(x_coords, y_coords))

        n_values, n_counts = np.unique(pmt_number, return_counts=True)
        all_pmt_numbers = np.arange(0, 2304)
        count_dict = {pmt_num: 0 for pmt_num in all_pmt_numbers}
        for value, count in zip(n_values, n_counts):
            count_dict[value] = count

        n_counts = np.array(list(count_dict.values()))

        df = pd.DataFrame(list(zip(x_coords, y_coords)), columns=['X', 'Y'])
        unique_x = sorted(df['X'].unique())
        unique_y = sorted(df['Y'].unique())

        freq_matrix = np.zeros((len(unique_y), len(unique_x)))
        for idx, (x, y) in enumerate(coordinates):
            ix = unique_x.index(x)
            iy = unique_y.index(y)
            freq_matrix[iy, ix] = n_counts[idx]

        freq_df = pd.DataFrame(freq_matrix, index=unique_y, columns=unique_x)

        if freq_df.empty:
            print(f"Frequency DataFrame is empty for {filename}.")
            return

        plt.figure(figsize=(10, 8))
        sns.heatmap(freq_df, cmap='viridis', fmt=".0f", linewidths=.5, square=True)
        plt.title(f'PMT Heatmap - {filename}')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')

        image_path = os.path.join(self.new_folder, f'{filename[:-4]}.png')
        plt.savefig(image_path)
        plt.close()

    def process_all_files(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.npy'):
                self.process_file(filename)

