# -*- coding: utf-8 -*-
"""
@ProjectName: ffmpeg_dev
@FileName:  video_pro
@Autor:  victor
@Date:  2023/12/12 22:59
"""

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ffmpeg_pro import Ui_MainWindow
from videoprocess import videoProc, VideoProcessor


class videoPro(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(videoPro, self).__init__()
        self.setupUi(self)
        self._cmd = 1
        self.videoHandler = videoProc  # type: VideoProcessor

        self._filepath = ''
        self._filename = ''

        self.init_UI()

        # 将文本框设置为接受拖放
        self.linEdit_InputPath.setAcceptDrops(True)

        # 连接拖放事件处理函数
        self.linEdit_InputPath.dragEnterEvent = self.dragEnterEvent
        self.linEdit_InputPath.dropEvent = self.dropEvent

        self.treeWidget.itemClicked.connect(self.on_treeWidget_itemClicked_Slot)

        self.btn_generate.clicked.connect(self.on_btn_generate_clicked_Slot)

        self.dSpBox_speed.valueChanged.connect(self.on_dSpBox_speed_valueChanged_Slot)
        self.linEdit_framenum.textChanged.connect(self.on_linEdit_framenum_textChanged_Slot)

    def init_UI(self):
        self.setWindowTitle("MultiMedia-Processing-Tools             Power by FogSalary")
        self.stackedWidget.setCurrentIndex(0)

    def set_current_page(self, page_name):
        print(page_name)
        if page_name == '视频倍速':
            # self.stackedWidget.setCurrentIndex(0)
            self._cmd = 1
        elif page_name == '视频帧提取':
            # self.stackedWidget.setCurrentIndex(1)
            self._cmd = 2
        elif page_name == '视频合并':
            # self.stackedWidget.setCurrentIndex(2)
            self._cmd = 3
        elif page_name == '视频拼接':
            # self.stackedWidget.setCurrentIndex(3)
            self._cmd = 4
        elif page_name == '视频裁剪':
            # self.stackedWidget.setCurrentIndex(4)
            self._cmd = 5
        elif page_name == '视频去除音频':
            # self.stackedWidget.setCurrentIndex(5)
            self._cmd = 6
        elif page_name == '视频水印':
            # self.stackedWidget.setCurrentIndex(6)
            self._cmd = 7
        elif page_name == '图片水印':
            self._cmd = 8
        elif page_name == '连环图':
            self._cmd = 9
        elif page_name == '图片缩放':
            self._cmd = 10

        self.stackedWidget.setCurrentIndex(self._cmd - 1)

    def on_treeWidget_itemClicked_Slot(self, item, column):
        selected_page = item.text(column)
        self.set_current_page(selected_page)

    def on_btn_generate_clicked_Slot(self):
        output_path = os.path.dirname(self.linEdit_InputPath.text())
        print(output_path)
        input_file = self.linEdit_InputPath.text()
        output_file = self.lineEdit.text()
        if self._cmd == 1:
            # 视频倍速
            ratio = self.dSpBox_speed.text()
            # if output_file == '':
            #     output_file = os.path.splitext(input_file.split('/')[-1])[0] + "_" + ratio + os.path.splitext(input_file.split('/')[-1])[1]
            #     output_file = os.path.join(output_path, output_file)
            output_file = os.path.join(output_path, output_file)
            self.videoHandler.change_video_speed(input_file, output_file, float(ratio))
            print("output %s" % output_file)
        elif self._cmd == 2:
            # 视频帧提取
            # self.videoHandler.extract_frames(input_file, os.path.join(output_path, 'extract_vedio'))
            save_path = self.lineEdit.text()
            framenum = int(self.linEdit_framenum.text())
            self.videoHandler.extract_frames(self._filepath, save_path, framenum / (
                        self.videoHandler._video_frame_count / self.videoHandler._video_frame_rate))
        elif self._cmd == 9:
            input_path = self.linEdit_InputPath.text()
            output_path = os.path.dirname(input_path)
            input_files = []
            for root, dir, files in os.walk(input_path):
                input_files = [os.path.join(input_path, file) for file in files]
                self.linEdit_mergePicNum.setText(str(len(input_files)))
            merge_row = int(self.linEdit_mergePicRow.text())
            merge_col = int(self.linEdit_mergePicCol.text())
            # 连环图
            self.videoHandler.videoMerge(input_files, os.path.join(output_path, 'merge_result.png'), [merge_row, merge_col])

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()

        # 检查是否有文件被拖放
        if mime_data.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()

        file_path = ''
        # 获取拖放的第一个文件路径
        if mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()
            self.linEdit_InputPath.setText(file_path)

        self._filepath = file_path
        self._filename = os.path.basename(file_path)
        file_type = os.path.splitext(self._filename)[-1]
        if file_type == '.mp4':
            self.textEdit.clear()
            recv = self.videoHandler.get_video_info(file_path)
            self.textEdit.setText(recv)

    def on_dSpBox_speed_valueChanged_Slot(self):
        value = self.dSpBox_speed.value()
        filename_1 = os.path.splitext(self._filename)[0]
        filename_2 = os.path.splitext(self._filename)[-1]
        file_name = filename_1 + ("_x%d" % int(value)) + filename_2
        self.lineEdit.setText(file_name)

    def on_linEdit_framenum_textChanged_Slot(self):
        framenum = int(self.linEdit_framenum.text())
        filename = os.path.splitext(self._filename)[0]
        output_path = os.path.dirname(self._filepath)
        save_path = os.path.join(output_path, filename + '_frames')
        # os.makedirs(save_path, exist_ok=True)
        self.lineEdit.setText(save_path)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = videoPro()
    w.show()
    sys.exit(app.exec_())
