import logging
import sys
from bandit_bot import BanditBot


if __name__ == '__main__':
    # 通过命令行参数设置日志级别
    level = sys.argv[1] if len(sys.argv) > 1 else 'INFO'
    if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        level = 'INFO'
    logging.basicConfig(level=level)
    bot = BanditBot()
    bot.run()
