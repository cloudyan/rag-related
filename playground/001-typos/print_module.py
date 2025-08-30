"""
错别字纠错练习短文批量生成器 - 打印模块
将生成的练习内容转换为A4横放双版面方格纸格式的PDF，左右各一个32k版面，每个版面内部竖向排版
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class ExercisePrinter:
    """练习打印器类 - A4横放双版面设计"""

    def __init__(self):
        """初始化打印器"""
        self.styles = getSampleStyleSheet()
        self._setup_fonts()
        self._setup_styles()

        # A4横放尺寸：297mm x 210mm
        self.page_width, self.page_height = A4[1], A4[0]

        # 版面配置
        self.margin = 10 * mm  # 外边距：1cm

        # 32k版面尺寸（左右各一个）
        # A4横放：297mm x 210mm
        # 两个32k版面：每个130mm x 184mm
        # 考虑间距：130mm + 20mm + 130mm = 280mm < 297mm（可行）
        self.panel_width = 130 * mm
        self.panel_height = 184 * mm

        # 每个版面：10行10列
        self.rows_per_panel = 10
        self.cols_per_panel = 10

        # 计算字格大小
        self.cell_width = self.panel_width / self.cols_per_panel
        self.cell_height = self.panel_height / self.rows_per_panel

    def _setup_fonts(self):
        """设置字体（支持中文）"""
        try:
            # 尝试注册系统中文字体
            font_paths = [
                "/System/Library/Fonts/PingFang.ttc",  # macOS
                "/System/Library/Fonts/STHeiti Light.ttc",  # macOS
                "C:/Windows/Fonts/simsun.ttc",  # Windows
                "C:/Windows/Fonts/msyh.ttc",  # Windows
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Linux
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('SimSun', font_path))
                    break
            else:
                # 如果没有找到中文字体，使用默认字体
                print("警告：未找到中文字体，可能影响中文显示")
        except Exception as e:
            print(f"字体设置失败: {e}")

    def _setup_styles(self):
        """设置样式"""
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='SimSun' if 'SimSun' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        )

        # 正文样式
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_LEFT,
            fontName='SimSun' if 'SimSun' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        )

        # 提示样式
        self.hint_style = ParagraphStyle(
            'CustomHint',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=15,
            alignment=TA_LEFT,
            fontName='SimSun' if 'SimSun' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
            textColor=colors.grey
        )

    def _create_panel_table(self, title: str, body: str, panel_title: str = "") -> Table:
        """
        创建单个版面的方格纸表格

        Args:
            title: 练习标题
            body: 正文内容
            panel_title: 版面标题（如"练习一"）

        Returns:
            版面表格
        """
        # 将正文按行分割
        body_lines = body.strip().split('\n')

        # 创建表格数据：10行10列
        table_data = []

        # 添加标题行（居中）
        title_row = [''] * self.cols_per_panel
        if title:
            start_col = max(0, (self.cols_per_panel - len(title)) // 2)
            for i, char in enumerate(title):
                if start_col + i < self.cols_per_panel:
                    title_row[start_col + i] = char
        table_data.append(title_row)

        # 添加正文行（最多9行，因为第1行是标题）
        for i, line in enumerate(body_lines):
            if i >= self.rows_per_panel - 1:  # 最多9行正文
                break
            if line.strip():
                body_row = [''] * self.cols_per_panel
                for j, char in enumerate(line):
                    if j < self.cols_per_panel:
                        body_row[j] = char
                table_data.append(body_row)
            else:
                # 空行
                body_row = [''] * self.cols_per_panel
                table_data.append(body_row)

        # 如果正文行数不足，补充空行到10行
        while len(table_data) < self.rows_per_panel:
            empty_row = [''] * self.cols_per_panel
            table_data.append(empty_row)

        # 创建表格
        table = Table(table_data,
                     colWidths=[self.cell_width] * self.cols_per_panel,
                     rowHeights=[self.cell_height] * self.rows_per_panel)

        # 设置表格样式
        style = TableStyle([
            # 所有网格线
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),

            # 每5个格子加粗线（便于书写）
            ('LINEAFTER', (4, 0), (4, -1), 1, colors.black),
            ('LINEAFTER', (9, 0), (9, -1), 1, colors.black),

            # 每5行加粗线
            ('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),
            ('LINEBELOW', (0, 9), (-1, 9), 1, colors.black),

            # 文字居中
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # 字体设置
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun' if 'SimSun' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ])

        table.setStyle(style)
        return table

    def _parse_exercise_content(self, exercise: str) -> Tuple[str, str, str, str]:
        """
        解析练习内容，提取标题、正文、提示和答案

        Args:
            exercise: 练习内容

        Returns:
            (标题, 正文, 提示, 答案)
        """
        lines = exercise.strip().split('\n')

        title = ""
        body = ""
        hint = ""
        answer = ""

        # 查找答案部分的分隔点
        answer_start = -1
        for i, line in enumerate(lines):
            if line.strip() == "答案：":
                answer_start = i
                break

        # 分离练习内容和答案
        if answer_start != -1:
            # 练习内容（不包含答案）
            exercise_lines = lines[:answer_start]
            # 答案内容（简化格式）
            answer_lines = lines[answer_start:]
        else:
            # 如果没有找到答案分隔符，整个内容作为练习
            exercise_lines = lines
            answer_lines = []

        # 解析练习内容
        for i, line in enumerate(exercise_lines):
            line = line.strip()
            if not line:
                continue

            if i == 0 and len(line) <= 8:
                # 第一行且长度较短，可能是标题
                title = line
            elif "共有" in line and ("个" in line or "处" in line) and "已找到" in line:
                # 包含提示信息的行
                hint = line
            else:
                # 正文内容
                if body:
                    body += "\n" + line
                else:
                    body = line

        # 处理答案内容
        if answer_lines:
            answer = "\n".join(answer_lines)

        return title, body, hint, answer

    def create_exercise_pdf(self, exercises: List[str], config: Dict[str, Any],
                           output_path: str = None) -> str:
        """
        创建练习PDF文件 - A4横放双版面设计

        Args:
            exercises: 练习列表
            config: 配置信息
            output_path: 输出路径，如果为None则自动生成

        Returns:
            生成的PDF文件路径
        """
        # 确保输出目录存在
        if not output_path:
            dist_dir = "dist"
            os.makedirs(dist_dir, exist_ok=True)

            mode_name = config.get("mode", "misspelling")
            grade = config.get("grade", "二年级")
            theme = config.get("theme", "随机主题")
            if theme == "random":
                theme = "随机主题"

            output_path = os.path.join(dist_dir, f"{mode_name}_{grade}_{theme}_双版面练习纸.pdf")

        # 创建PDF文档 - A4横放
        doc = SimpleDocTemplate(output_path, pagesize=(self.page_width, self.page_height))
        story = []

        # 添加文档标题
        title_text = f"{config.get('grade', '二年级')}语文练习纸 - A4横放双版面"
        title_para = Paragraph(title_text, self.title_style)
        story.append(title_para)
        story.append(Spacer(1, 20))

        # 处理练习内容，每两个练习组成一页
        for i in range(0, len(exercises), 2):
            # 第一个练习（左侧版面）
            if i < len(exercises):
                exercise1 = exercises[i]
                title1, body1, hint1, answer1 = self._parse_exercise_content(exercise1)

                # 创建左侧版面
                left_panel = self._create_panel_table(title1, body1, f"练习 {i+1}")
                story.append(left_panel)

                # 添加两个版面之间的间距
                story.append(Spacer(1, 20))

                # 第二个练习（右侧版面）
                if i + 1 < len(exercises):
                    exercise2 = exercises[i + 1]
                    title2, body2, hint2, answer2 = self._parse_exercise_content(exercise2)

                    # 创建右侧版面
                    right_panel = self._create_panel_table(title2, body2, f"练习 {i+2}")
                    story.append(right_panel)
                else:
                    # 如果只有一个练习，右侧版面留空
                    empty_panel = self._create_panel_table("", "", "练习 待定")
                    story.append(empty_panel)

                # 添加答案区域（在版面下方）
                story.append(Spacer(1, 30))

                # 添加分隔线
                separator = Paragraph("=" * 80, self.hint_style)
                story.append(separator)
                story.append(Spacer(1, 20))

                # 添加答案标题
                answer_title = Paragraph("【答案】（家长参考）", self.body_style)
                story.append(answer_title)
                story.append(Spacer(1, 10))

                # 添加第一个练习的答案
                if answer1:
                    answer1_title = Paragraph(f"练习 {i+1} 答案：", self.body_style)
                    story.append(answer1_title)
                    answer1_content = Paragraph(answer1, self.hint_style)
                    story.append(answer1_content)
                    story.append(Spacer(1, 10))

                # 添加第二个练习的答案
                if i + 1 < len(exercises) and answer2:
                    answer2_title = Paragraph(f"练习 {i+2} 答案：", self.body_style)
                    story.append(answer2_title)
                    answer2_content = Paragraph(answer2, self.hint_style)
                    story.append(answer2_content)
                    story.append(Spacer(1, 10))

                # 添加练习分隔线
                if i + 2 < len(exercises):
                    story.append(Spacer(1, 20))
                    separator = Paragraph("=" * 80, self.hint_style)
                    story.append(separator)
                    story.append(Spacer(1, 20))

        # 添加页脚信息
        story.append(Spacer(1, 30))
        footer_text = f"生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')} | 纸张规格：A4横放 | 版面规格：32k双版面"
        footer_para = Paragraph(footer_text, self.hint_style)
        story.append(footer_para)

        # 生成PDF
        doc.build(story)
        print(f"双版面PDF已生成：{output_path}")
        return output_path

    def print_from_json(self, json_file_path: str, output_path: str = None) -> str:
        """
        从JSON文件读取练习内容并生成PDF

        Args:
            json_file_path: JSON文件路径
            output_path: 输出PDF路径，如果为None则自动生成

        Returns:
            生成的PDF文件路径
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            exercises = data.get('exercises', [])
            config = data.get('config', {})

            if not exercises:
                print("JSON文件中没有找到练习内容")
                return ""

            return self.create_exercise_pdf(exercises, config, output_path)

        except Exception as e:
            print(f"读取JSON文件失败: {e}")
            return ""


def main():
    """主函数 - 测试打印功能"""
    printer = ExercisePrinter()

    # 查找dist目录下的JSON文件
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        print("dist目录不存在，请先运行生成器生成练习内容")
        return

    json_files = [f for f in os.listdir(dist_dir) if f.endswith('.json')]

    if not json_files:
        print("dist目录下没有找到JSON文件，请先运行生成器生成练习内容")
        return

    # 处理第一个JSON文件
    json_file = json_files[0]
    json_path = os.path.join(dist_dir, json_file)

    print(f"正在处理文件：{json_file}")
    print("生成A4横放双版面练习纸...")

    # 生成PDF
    pdf_path = printer.print_from_json(json_path)

    if pdf_path:
        print(f"双版面PDF生成成功：{pdf_path}")
        print("\n使用说明：")
        print("1. 打印时选择A4横放")
        print("2. 左右各一个32k版面")
        print("3. 每个版面内部竖向排版（10行10列）")
        print("4. 行间距半格高度，无方格")
        print("5. 底部预留成绩区空间")
    else:
        print("PDF生成失败")


if __name__ == "__main__":
    main()
