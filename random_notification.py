import random
import time
import threading
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

class NotificationSystem(QObject):
    notification_signal = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.app.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setVisible(True)
        
        # 创建托盘菜单
        tray_menu = QMenu()
        quit_action = QAction("退出")
        quit_action.triggered.connect(self.app.quit)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        
        # 连接信号
        self.notification_signal.connect(self.show_notification)
        
        # 启动定时器
        self.next_delay = self.generate_random_delay()
        print(f"脚本已启动，首次通知将在 {self.next_delay} 秒后显示")
        QTimer.singleShot(self.next_delay * 1000, self.show_next_notification)
    
    def generate_random_delay(self):
        """生成0-600秒的随机延迟时间"""
        return random.randint(0, 600)
    
    def show_next_notification(self):
        """显示下一个通知"""
        self.notification_signal.emit(
            "随机提醒：请专注于你的任务owo",
            f"这是一个定时通知！\n下次通知将在 {self.next_delay//60} 分 {self.next_delay%60} 秒后显示"
        )
        print(f"通知已显示，下次将在 {self.next_delay} 秒后执行")
        
        # 生成新的延迟时间并设置下一个定时器
        self.next_delay = self.generate_random_delay()
        QTimer.singleShot(self.next_delay * 1000, self.show_next_notification)
    
    def show_notification(self, title, message):
        """显示通知"""
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 3000)

def main():
    # 创建通知系统
    notification_system = NotificationSystem()
    
    # 运行应用
    sys.exit(notification_system.app.exec_())

if __name__ == "__main__":
    # 在单独的线程中运行Qt应用
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("脚本已停止")
        sys.exit(0)