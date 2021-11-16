import sys
import pathlib

from loguru import logger


# from OneForAll - https://github.com/shmilylty/OneForAll

# 路径设置
relative_directory = pathlib.Path(__file__).parent.parent  # CarvedBrink根目录
result_save_path = relative_directory.joinpath("results")  # 结果保存目录
log_save_dir = result_save_path.joinpath("log")  # 日志保存目录
log_path = log_save_dir.joinpath("{time}.log")  # 日志保存路径

# 日志配置
# 终端日志输出格式
stdout_fmt = (
    "<cyan>{time:HH:mm:ss,SSS}</cyan> "
    "[<level>{level: <5}</level>] "
    "<blue>{module}</blue>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
# 日志文件记录格式
logfile_fmt = (
    "<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green> "
    "[<level>{level: <5}</level>] "
    "<cyan>{process.name}({process.id})</cyan>:"
    "<cyan>{thread.name: <18}({thread.id: <5})</cyan> | "
    "<blue>{name}</blue>.<blue>{function}</blue>:"
    "<blue>{line}</blue> - <level>{message}</level>"
)

logger.remove()
logger.level(name="TRACE", color="<cyan><bold>", icon="✏️")
logger.level(name="DEBUG", color="<blue><bold>", icon="🐞 ")
logger.level(name="INFOR", no=20, color="<green><bold>", icon="ℹ️")
logger.level(name="QUITE", no=25, color="<green><bold>", icon="🤫 ")
logger.level(name="ALERT", no=30, color="<yellow><bold>", icon="⚠️")
logger.level(name="ERROR", color="<red><bold>", icon="❌️")
logger.level(name="FATAL", no=50, color="<RED><bold>", icon="☠️")

# 如果你想在命令终端静默运行，可以将以下一行中的level设置为QUITE
# 命令终端日志级别默认为INFOR
logger.add(sys.stderr, level="DEBUG", format=stdout_fmt, enqueue=True)
# 日志文件默认为级别为DEBUG
logger.add(
    log_path,
    level="DEBUG",
    format=logfile_fmt,
    enqueue=True,
    encoding="utf-8",
    rotation="12:00",
    retention="7 days",
)
