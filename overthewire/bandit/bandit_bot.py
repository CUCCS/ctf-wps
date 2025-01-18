import paramiko
import time
import logging
from config import HOST, PORT, USERNAME_PREFIX, INITIAL_PASSWORD
from solutions import solutions, greps

class BanditBot:
    def __init__(self):
        self.ssh = None
        self.current_level = 0
        self.passwords = {0: INITIAL_PASSWORD}
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='bandit_bot.log'
        )
        
    def connect(self, level):
        """连接到指定关卡"""
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            username = f"{USERNAME_PREFIX}{level}"
            password = self.passwords.get(level)
            
            self.ssh.connect(
                hostname=HOST,
                port=PORT,
                username=username,
                password=password
            )
            
            logging.info(f"Successfully connected to level {level}")
            return True
            
        except Exception as e:
            logging.error(f"Connection failed for level {level}: {str(e)}")
            return False
            
    def execute_command(self, wp, grep):
        """执行命令并返回结果"""
        try:
            command = f"{wp} | {grep}"
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read().decode().strip()
        except Exception as e:
            logging.error(f"Command execution failed: {str(e)}")
            return None
            
    def solve_level(self, level):
        """解决特定关卡"""
        if not self.connect(level):
            return False
            
        if level in solutions:
            # 针对需要交互式输入的关卡
            if level == 15:
                try:
                    # 获取交互式 shell
                    channel = self.ssh.invoke_shell()
                    # 等待 shell 准备就绪
                    time.sleep(1)
                    
                    # 发送命令
                    channel.send(solutions[level] + '\n')
                    time.sleep(2)  # 等待命令执行
                    
                    # 发送密码
                    channel.send(self.passwords[level] + '\n')
                    time.sleep(1)  # 等待响应
                    
                    # 读取输出
                    output = ''
                    while channel.recv_ready():
                        output += channel.recv(1024).decode()
                    
                    # 等待终端输出 bandit15 则输入 exit 退出会话
                    channel.send("exit\n")
                    time.sleep(1)

                    # 从 exit 指令之前的输出中提取密码
                    logging.info(output)
                    result = output.strip().split('\n')[-4] # TOFIX 硬编码
                    if result:
                        self.passwords[level + 1] = result
                        logging.info(f"Level {level} completed. Password found: {result}")
                        return True
                        
                except Exception as e:
                    logging.error(f"Interactive command failed: {str(e)}")
                    return False
                finally:
                    channel.close()

            # 处理其他普通关卡
            result = self.execute_command(solutions[level], greps[level])
            if result:
                self.passwords[level + 1] = result
                logging.info(f"Level {level} completed. Password found: {result}")
                return True
                
        return False
        
    def run(self):
        """运行机器人"""
        while True:
            if not self.solve_level(self.current_level):
                break
            self.current_level += 1
            time.sleep(1)  # 避免请求过于频繁
            
        logging.info(f"Bot stopped at level {self.current_level}")
