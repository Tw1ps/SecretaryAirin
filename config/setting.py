import pathlib


# 路径设置
root_directory = pathlib.Path(__file__).parent.parent  # CarvedBrink根目录路径
result_save_path = root_directory.joinpath("results")  # 结果保存目录
data_storage_dir = root_directory.joinpath("data")  # 数据存放目录

# 结果保存设置
result_save_format = "csv"
result_save_encode = "utf-8"

# dns 请求并发数
async_semaphore = 50
