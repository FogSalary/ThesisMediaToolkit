# -*- coding: utf-8 -*-
"""
@ProjectName: ffmpeg_dev
@FileName:  videoprocess
@Autor:  victor
@Date:  2023/12/12 0:12
"""

import ffmpeg
import sys
import os
import numpy as np

class VideoProcessor():

    def __init__(self):
        self._video_frame_rate = 0
        self._video_frame_count = 0

    def change_video_speed(self, input_file, output_file, speed):
        # 使用ffmpeg进行视频倍速处理
        ffmpeg.input(input_file).output(output_file, vf='setpts={:.2f}*PTS'.format(1.0 / speed)).run()

    def extract_frames(self, input_file, output_folder, fps):
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Use ffmpeg to extract frames
        # ffmpeg.input(input_file).output(os.path.join(output_folder, 'frame%04d.png')).run()
        ffmpeg.input(input_file).output(os.path.join(output_folder, 'frame%04d.jpg'), vf='fps=%f' % round(fps, 2), start_number=1).run()

    def get_video_info(self, video_path: str):
        '''
            获取视频信息，包括视频的 width*height 以及总帧数
        :param video_path: 输入视频文件路径 'xxx.mp4'
        :return:
        '''
        try:
            probe = ffmpeg.probe(video_path)
            video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            if video_info is None:
                print('No video stream found', file=sys.stderr)
                sys.exit(1)

            frame_rate = eval(video_info['avg_frame_rate'])
            frame_rate = round(frame_rate, 2)
            width = int(video_info['width'])
            height = int(video_info['height'])
            frame_count = int(video_info['nb_frames'])
            self._video_frame_rate = frame_rate
            self._video_frame_count = frame_count

        except ffmpeg.Error as e:
            print(e.stderr, file=sys.stderr)
            sys.exit(1)

        message = f"file_name: {os.path.basename(video_path)}\nframe_rate: {frame_rate}\nwidth: {width}\nheight: {height}\nframe_count: {frame_count}\n"

        return message

    def addText(self, in_filename: str, out_filename: str, text: str):
        '''
            在视频中添加文字说明
        :param in_filename: 输入视频 path
        :param out_filename: 输出视频 path
        :param text: 添加的文字说明内容
        :return:
        '''
        stream = ffmpeg.input(in_filename)  # 读取视频文件
        # 添加文字说明
        stream = ffmpeg.drawtext(stream, text, x=10, y=10,
                                 fontsize=45, fontcolor='Gold',
                                 box=True, boxcolor='Green@0.0')
        stream = ffmpeg.output(stream, out_filename)  # 输出视频文件
        stream = ffmpeg.overwrite_output(stream)  # 替换原有文件不提示
        ffmpeg.run(stream)  # 执行

    def getVideoPng(self,in_filename: str,out_picname: str):
        '''
            处理视频文件，获取所有帧的图片数据
        :param filename: 输入视频 path
        :param out_picname: 输出图片 path
        :return:
        '''
        (
            ffmpeg
            .input(in_filename)
            # .filter('select', 'gte(n,100)')
            # .output(out_picname, vframes=1)
            .filter('fps', fps=10,round='up')
            .output('./pic_output/output_%05d.png',start_number=0,format='image2')
            .run()
        )

    def videoCrop(self,in_filename: str, out_filename: str, whxy: list):
        '''
            对视频文件进行裁剪，保存为新文件
        :param in_filename:
        :param whxy: w 为目标 width, h 为目标 height, x,y 为起始像素坐标点
        :return:
        '''
        (
            ffmpeg
            .input(in_filename)
            .filter('crop', w=whxy[0], h=whxy[1], x=whxy[2], y=whxy[3])
            .output(out_filename)
            .run()
        )

    def getOneFrame(self,in_filename: str, out_picname: str):
        '''
            从视频中获取一帧图片
        :param in_filename: 输入视频 path
        :param out_picname: 输出图片 path
        :return:
        '''
        (
            ffmpeg
            .input(in_filename)
            .filter('select', 'gte(n,100)')
            .output(out_picname, vframes=1)
            .overwrite_output()
            .run()
        )

    def drawBoxInPic(self,in_picname: str, out_picname: str, whxy: list):
        '''
            在图片中绘制矩形框，用于测试裁剪区域范围是否符合预期
        :param in_picname: 输入图片 path
        :param out_picname: 输出图片 path
        :param whxy: weight,height,x,y 分别为矩形框的 w 和 h,以及矩形框起始点 x,y
        :return:
        '''
        # 绘制矩形框
        (
            ffmpeg
            .input(in_picname)
            .filter('drawbox', x=whxy[2], y=whxy[3], width=whxy[0], height=whxy[1],
                    color='red', thickness=5)
            .output(out_picname)
            .overwrite_output()
            .run()
        )

    def videoMerge2by2(self,in_filenames: list, out_filename: str):
        '''
            视频合并案例，还未整合成函数
        :param in_filename:
        :return:
        '''
        inputs = [ffmpeg.input(file) for file in in_filenames]
        print(len(inputs))
        # 视频拼接
        top = ffmpeg.filter([inputs[0], inputs[1]], 'hstack')
        bottom = ffmpeg.filter([inputs[2], inputs[3]], 'hstack')

        output = ffmpeg.filter([top, bottom], 'vstack')
        output = ffmpeg.output(output, out_filename)
        # 输出
        ffmpeg.run(output)

    def videoMerge2by3(self,in_filenames: list, out_filename: str):
        '''
            视频合并案例，还未整合成函数
        :param in_filename:
        :return:
        '''
        inputs = [ffmpeg.input(file) for file in in_filenames]
        print(len(inputs))
        # 视频拼接
        top = ffmpeg.filter([inputs[0], inputs[1]], 'hstack')
        top = ffmpeg.filter([top, inputs[2]], 'hstack')
        bottom = ffmpeg.filter([inputs[3], inputs[4]], 'hstack')
        bottom = ffmpeg.filter([bottom, inputs[5]], 'hstack')

        output = ffmpeg.filter([top, bottom], 'vstack')
        output = ffmpeg.output(output, out_filename)
        # 输出
        ffmpeg.run(output)

    def videoMerge(self,in_filenames: list, out_filename, mergesize: list):
        '''
            视频合并函数
        :param in_filenames: 待合并的视频路径
        :param out_filename: 合并后视频输出路径
        :param mergesize:  合并的布局 n*m，[n,m]
        :return:
        '''
        inputs = [ffmpeg.input(file) for file in in_filenames]  # 依次读取输入视频，存为列表
        input_nums = len(inputs)  # 获取输入视频个数
        row_num, col_num = mergesize[0], mergesize[1]  # 目标连环图长宽
        row_stream = []
        if row_num * col_num != input_nums:
            print("输入视频总数目与目标布局所需视频数目不一致，请检查！")
            return
        tmp = 0
        for i in range(row_num):
            if col_num == 1:
                row_stream.append(inputs[i])
            else:
                for j in range(col_num - 1):
                    if j == 0:
                        tmp = ffmpeg.filter([inputs[j + i * col_num], inputs[j + 1 + i * col_num]], 'hstack')
                    else:
                        tmp = ffmpeg.filter([tmp, inputs[j + 1 + i * col_num]], 'hstack')
                    if j == col_num - 2:
                        row_stream.append(tmp)
        output = 0
        if row_num == 1:
            output = row_stream[0]
        else:
            for i in range(row_num - 1):
                if i == 0:
                    output = ffmpeg.filter([row_stream[i], row_stream[i + 1]], 'vstack')
                else:
                    output = ffmpeg.filter([output, row_stream[i + 1]], 'vstack')

        # output = ffmpeg.filter([top, bottom], 'vstack')
        output = ffmpeg.output(output, out_filename)
        output = ffmpeg.overwrite_output(output)
        # 输出
        ffmpeg.run(output)

    def picScale(self,in_picname: str, out_picname: str, scale: int):
        '''
            图片缩放操作函数
        :param in_picname:  待处理图片 path
        :param out_picname: 处理完成后输出图片 path
        :param scale: 缩放系数
        :return:
        '''
        (
            ffmpeg
            .input(in_picname)
            .filter('scale', width='iw/' + str(scale), height='ih/' + str(scale))
            .output(out_picname)
            .overwrite_output()
            .run()
        )

    def addTimeLabel(self,in_filename: str, out_filename, text: str):
        '''
            为图片添加时间戳
        :param in_filename:
        :param out_filename:
        :param text:
        :return:
        '''
        # probe = ffmpeg.probe(in_filename)
        # video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        input = ffmpeg.input(in_filename)
        # width = int(video_stream['width'])
        # height = int(video_stream['height'])
        input = ffmpeg.drawtext(input, text, x=0, y=0, fontsize=30, fontcolor='Black',
                                box=True, boxcolor='White')
        output = ffmpeg.output(input, out_filename)
        output = ffmpeg.overwrite_output(output)
        ffmpeg.run(output)

    def addLabLogo(in_filename: str, out_filename: str, in_image: str, scale: int):
        '''
            对输入视频添加实验室的 LOGO 图片
        :param in_filename: 输入视频文件 path
        :param out_filename: 输出视频文件 path
        :param in_image: 输入 LOGO 图片 path
        :param scale: LOGO 图片缩放系数
        :return: None
        '''
        input = ffmpeg.input(in_filename)
        overlay = ffmpeg.input(in_image)
        video_probe = ffmpeg.probe(in_filename)['streams'][0]
        img_probe = ffmpeg.probe(in_image)['streams'][0]
        img_width = img_probe['width']
        img_width_scale = img_width / scale
        video_width = video_probe['width']
        overlay = ffmpeg.filter(overlay, 'scale', width='iw/' + str(scale), height='ih/' + str(scale))
        tmp = ffmpeg.overlay(input, overlay, x=video_width - img_width_scale, y=0)
        output = ffmpeg.output(tmp, out_filename)
        output = ffmpeg.overwrite_output(output)
        ffmpeg.run(output)

videoProc = VideoProcessor()

if __name__ == '__main__':
    input_file = "vedio.mp4"
    output_file = "vedio_2.mp4"
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, output_file)
    ffmpeg.run(stream)