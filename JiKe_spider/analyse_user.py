import matplotlib.pyplot as plt
import pandas as pd


class AnalyseUser:
    def __init__(self, data_path, compare_data_path=None):
        self.data = pd.read_excel(data_path)
        self.compare_data = pd.read_excel(compare_data_path) if compare_data_path else {}

    def draw_plot(self):
        create_time_arr = self.data['create_time'].to_numpy()
        like_arr = self.data['like'].to_numpy()

        # 设置中文字体显示
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        if self.compare_data:
            c_create_time_arr = self.compare_data['create_time'].to_numpy()
            c_like_arr = self.compare_data['like'].to_numpy()
            plt.plot(c_create_time_arr, c_like_arr, color='green', linestyle='-.',
                     label=self.compare_data.iloc[0]['user'])
        plt.plot(create_time_arr, like_arr, color='red', linestyle='--', label=self.data.iloc[0]['user'])
        plt.xticks(rotation=270)
        plt.title('date_like')
        plt.xlabel('date')
        plt.ylabel('like')
        plt.legend(loc='upper left')
        plt.show()

    def draw_subplot(self):

        create_time_arr = self.data['create_time'].to_numpy()
        like_arr = self.data['like'].to_numpy()
        area_arr = self.data['area'].to_list()
        # fig, axes = plt.subplots(nrows=2, ncols=2)
        # axe_1, axe_2, axe_3, axe_4 = axes.flatten()
        axe_1 = plt.subplot(221)
        axe_1.plot(create_time_arr, like_arr, label=self.data.iloc[0]['user'])
        plt.xticks(rotation=270)
        plt.title('date_like')
        plt.xlabel('date')
        plt.ylabel('like')
        plt.legend(loc='upper left')

        axe_2 = plt.subplot(222)
        labels = area_arr
        explode_list = []
        for i in range(len(area_arr)):
            explode_list.append(0.05)
        axe_2.pie(like_arr, labels=labels, explode=explode_list, autopct='%.2f%%')

        axe_3 = plt.subplot(223)
        group_dict = {}
        for idx in range(self.data.shape[0]):
            if self.data.iloc[idx]['area'] not in group_dict:
                group_dict[self.data.iloc[idx]['area']] = self.data.iloc[idx]['like']
            else:
                group_dict[self.data.iloc[idx]['area']] += self.data.iloc[idx]['like']
        axe_3.pie(group_dict.values(), labels=group_dict.keys(), autopct='%.2f%%')
        # 保存图片
        # plt.savefig('./analyse.jpg')
        plt.show()


if __name__ == '__main__':
    pass
