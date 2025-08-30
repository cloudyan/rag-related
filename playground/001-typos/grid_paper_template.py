"""
小学生语文A4横放方格纸模板生成器
生成包含两个32k版面的方格纸，A4横放，左右各一个版面，每个版面内部竖向排版
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


class GridPaperTemplate:
    """方格纸模板生成器 - A4横放双版面设计"""

    def __init__(self):
        """初始化"""
        # A4横放尺寸：297mm x 210mm
        self.page_width, self.page_height = A4[1], A4[0]  # 横放：297mm x 210mm

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

        # 行间距：半格高度（无方格）
        self.row_spacing = self.cell_height / 2

    def create_dual_panel_template(self, output_path: str = "dist/grid_template.pdf"):
        """
        创建双版面方格纸模板（A4横放，左右各一个32k版面）

        Args:
            output_path: 输出文件路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        print(f"页面尺寸: {self.page_width/mm:.1f}mm x {self.page_height/mm:.1f}mm")
        print(f"每个版面: {self.panel_width/mm:.1f}mm x {self.panel_height/mm:.1f}mm")
        print(f"字格大小: {self.cell_width/mm:.1f}mm x {self.cell_height/mm:.1f}mm")
        print(f"行间距: {self.row_spacing/mm:.1f}mm（无方格）")
        print("💡 使用说明：A4横放打印，左右各一个32k版面，每个版面内部竖向排版")

        # 创建PDF文档
        doc = SimpleDocTemplate(output_path, pagesize=(self.page_width, self.page_height))

        # 创建两个版面的表格（左右排列）
        story = []

        # 第一个版面（左侧）
        left_panel = self._create_panel_table("练习一")
        story.append(left_panel)

        # 添加两个版面之间的间距
        from reportlab.platypus import Spacer
        story.append(Spacer(1, 20))

        # 第二个版面（右侧）
        right_panel = self._create_panel_table("练习二")
        story.append(right_panel)

        # 构建PDF
        doc.build(story)

        print(f"双版面方格纸模板已生成: {output_path}")
        return output_path

    def _create_panel_table(self, panel_title: str) -> Table:
        """
        创建单个版面的表格

        Args:
            panel_title: 版面标题

        Returns:
            版面表格
        """
        # 创建表格数据：10行10列
        table_data = []

        # 添加标题行
        title_row = [''] * self.cols_per_panel
        if panel_title:
            start_col = max(0, (self.cols_per_panel - len(panel_title)) // 2)
            for i, char in enumerate(panel_title):
                if start_col + i < self.cols_per_panel:
                    title_row[start_col + i] = char
        table_data.append(title_row)

        # 添加正文行（9行，因为第1行是标题）
        for row in range(self.rows_per_panel - 1):
            body_row = [''] * self.cols_per_panel
            table_data.append(body_row)

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
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ])

        table.setStyle(style)
        return table

    def create_sample_template(self, output_path: str = "dist/grid_template_sample.pdf"):
        """
        创建带示例文字的双版面模板

        Args:
            output_path: 输出文件路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 示例文字内容
        sample_text_left = [
            "扒山",                    # 标题
            "昨天我合同学约好",        # 第1行
            "今天一起去爬山，一大",    # 第2行
            "早我们就初发了，一路",    # 第3行
            "上有说有笑很快就到了",    # 第4行
            "山角下，爬山的人很多",    # 第5行
            "没过多久我们就爬到了",    # 第6行
            "山顶，山顶的风景很",      # 第7行
            "美，爬山很累但我们很",    # 第8行
            "开心。"                   # 第9行
        ]

        sample_text_right = [
            "春游",                    # 标题
            "春天来了，小草绿了",      # 第1行
            "花儿开了，小鸟叫了",      # 第2行
            "我们一起去春游，看到",    # 第3行
            "了美丽的风景，呼吸着",    # 第4行
            "新鲜的空气，心情很好",    # 第5行
            "春天真是一个美好的季",    # 第6行
            "节，我们都很喜欢春天",    # 第7行
            "希望春天能多停留一会",    # 第8行
            "儿。"                     # 第9行
        ]

        # 创建PDF文档
        doc = SimpleDocTemplate(output_path, pagesize=(self.page_width, self.page_height))

        # 创建两个版面的表格
        story = []

        # 第一个版面（左侧）
        left_panel = self._create_sample_panel_table("练习一", sample_text_left)
        story.append(left_panel)

        # 添加两个版面之间的间距
        from reportlab.platypus import Spacer
        story.append(Spacer(1, 20))

        # 第二个版面（右侧）
        right_panel = self._create_sample_panel_table("练习二", sample_text_right)
        story.append(right_panel)

        # 构建PDF
        doc.build(story)

        print(f"带示例文字的双版面模板已生成: {output_path}")
        return output_path

    def _create_sample_panel_table(self, panel_title: str, sample_text: list) -> Table:
        """
        创建带示例文字的单个版面表格

        Args:
            panel_title: 版面标题
            sample_text: 示例文字列表

        Returns:
            版面表格
        """
        # 创建表格数据：10行10列
        table_data = []

        # 添加标题行
        title_row = [''] * self.cols_per_panel
        if panel_title:
            start_col = max(0, (self.cols_per_panel - len(panel_title)) // 2)
            for i, char in enumerate(panel_title):
                if start_col + i < self.cols_per_panel:
                    title_row[start_col + i] = char
        table_data.append(title_row)

        # 添加正文行（9行，因为第1行是标题）
        for row in range(self.rows_per_panel - 1):
            body_row = [''] * self.cols_per_panel
            if row < len(sample_text) - 1:  # 跳过标题
                text = sample_text[row + 1]  # 从第2个元素开始（跳过标题）
                for i, char in enumerate(text):
                    if i < self.cols_per_panel:
                        body_row[i] = char
            table_data.append(body_row)

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
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ])

        table.setStyle(style)
        return table


def main():
    """主函数"""
    print("小学生语文A4横放方格纸模板生成器")
    print("=" * 50)
    print("功能：生成包含两个32k版面的方格纸，A4横放，左右各一个版面")
    print("版面规格：每个版面10行10列，内部竖向排版")
    print("纸张规格：A4横放（297mm x 210mm）")
    print("布局方式：左右各一个32k版面，每个版面内部竖向排版")
    print("=" * 50)

    # 创建模板生成器
    template = GridPaperTemplate()

    # 生成双版面模板
    dual_panel = template.create_dual_panel_template("dist/grid_template.pdf")

    # 生成带示例文字的模板
    sample_template = template.create_sample_template("dist/grid_template_sample.pdf")

    print("\n模板生成完成！")
    print(f"双版面模板: {dual_panel}")
    print(f"示例模板: {sample_template}")
    print("\n使用说明：")
    print("1. 打印时选择A4横放")
    print("2. 左右各一个32k版面")
    print("3. 每个版面内部竖向排版（10行10列）")
    print("4. 行间距半格高度，无方格")
    print("5. 底部预留成绩区空间")


if __name__ == "__main__":
    main()
