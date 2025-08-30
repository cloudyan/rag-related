"""
简单的小学生语文方格纸A4 PDF模板
生成标准的方格纸，方便填入文字和标点符号
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def create_grid_paper(output_path: str = "dist/方格纸.pdf"):
    """
    创建方格纸PDF模板

    Args:
        output_path: 输出文件路径
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # A4页面尺寸
    page_width, page_height = A4

    # 设置参数
    margin = 15 * mm  # 页边距
    grid_size = 7 * mm  # 每个方格的大小

    # 计算网格数量
    cols = int((page_width - 2 * margin) / grid_size)
    rows = int((page_height - 2 * margin) / grid_size)

    print(f"生成方格纸模板...")
    print(f"页面尺寸: A4 ({page_width/mm:.0f}mm x {page_height/mm:.0f}mm)")
    print(f"网格数量: {cols}列 x {rows}行")
    print(f"每个方格: {grid_size/mm:.0f}mm x {grid_size/mm:.0f}mm")

    # 创建网格数据
    grid_data = []
    for row in range(rows):
        grid_row = ["" for _ in range(cols)]
        grid_data.append(grid_row)

    # 创建表格
    table = Table(grid_data,
                 colWidths=[grid_size] * cols,
                 rowHeights=[grid_size] * rows)

    # 设置表格样式
    style = TableStyle([
        # 所有网格线
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),

        # 每5个格子加粗线（便于书写）
        ('LINEAFTER', (4, 0), (4, -1), 1, colors.black),
        ('LINEAFTER', (9, 0), (9, -1), 1, colors.black),
        ('LINEAFTER', (14, 0), (14, -1), 1, colors.black),
        ('LINEAFTER', (19, 0), (19, -1), 1, colors.black),
        ('LINEAFTER', (24, 0), (24, -1), 1, colors.black),
        ('LINEAFTER', (29, 0), (29, -1), 1, colors.black),

        # 每5行加粗线
        ('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),
        ('LINEBELOW', (0, 9), (-1, 9), 1, colors.black),
        ('LINEBELOW', (0, 14), (-1, 14), 1, colors.black),
        ('LINEBELOW', (0, 19), (-1, 19), 1, colors.black),
        ('LINEBELOW', (0, 24), (-1, 24), 1, colors.black),
        ('LINEBELOW', (0, 29), (-1, 29), 1, colors.black),
        ('LINEBELOW', (0, 34), (-1, 34), 1, colors.black),

        # 文字居中
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table.setStyle(style)

    # 创建PDF文档
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    doc.build([table])

    print(f"方格纸模板已生成: {output_path}")
    return output_path


def create_multi_page_grid_paper(output_path: str = "dist/方格纸_多页.pdf", pages: int = 10):
    """
    创建多页方格纸PDF模板

    Args:
        output_path: 输出文件路径
        pages: 页数
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # A4页面尺寸
    page_width, page_height = A4

    # 设置参数
    margin = 15 * mm
    grid_size = 7 * mm

    # 计算网格数量
    cols = int((page_width - 2 * margin) / grid_size)
    rows = int((page_height - 2 * margin) / grid_size)

    print(f"生成 {pages} 页方格纸模板...")
    print(f"每页网格数量: {cols}列 x {rows}行")

    # 创建PDF文档
    doc = SimpleDocTemplate(output_path, pagesize=A4)

    # 创建每页的内容
    story = []

    for page_num in range(pages):
        # 创建网格数据
        grid_data = []
        for row in range(rows):
            grid_row = ["" for _ in range(cols)]
            grid_data.append(grid_row)

        # 创建表格
        table = Table(grid_data,
                     colWidths=[grid_size] * cols,
                     rowHeights=[grid_size] * rows)

        # 设置表格样式
        style = TableStyle([
            # 所有网格线
            ('GRID', (0, 0), (-1, -1), 0.3, colors.black),

            # 每5个格子加粗线
            ('LINEAFTER', (4, 0), (4, -1), 1, colors.black),
            ('LINEAFTER', (9, 0), (9, -1), 1, colors.black),
            ('LINEAFTER', (14, 0), (14, -1), 1, colors.black),
            ('LINEAFTER', (19, 0), (19, -1), 1, colors.black),
            ('LINEAFTER', (24, 0), (24, -1), 1, colors.black),
            ('LINEAFTER', (29, 0), (29, -1), 1, colors.black),

            # 每5行加粗线
            ('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),
            ('LINEBELOW', (0, 9), (-1, 9), 1, colors.black),
            ('LINEBELOW', (0, 14), (-1, 14), 1, colors.black),
            ('LINEBELOW', (0, 19), (-1, 19), 1, colors.black),
            ('LINEBELOW', (0, 24), (-1, 24), 1, colors.black),
            ('LINEBELOW', (0, 29), (-1, 29), 1, colors.black),
            ('LINEBELOW', (0, 34), (-1, 34), 1, colors.black),

            # 文字居中
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

        table.setStyle(style)
        story.append(table)

        # 添加分页符（除了最后一页）
        if page_num < pages - 1:
            from reportlab.platypus import PageBreak
            story.append(PageBreak())

    # 构建PDF
    doc.build(story)

    print(f"多页方格纸模板已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    print("小学生语文方格纸A4 PDF模板生成器")
    print("=" * 50)

    # 生成单页模板
    single_page = create_grid_paper("dist/方格纸_单页.pdf")

    # 生成多页模板
    multi_page = create_multi_page_grid_paper("dist/方格纸_多页.pdf", 10)

    print("\n✅ 模板生成完成！")
    print(f"📄 单页模板: {single_page}")
    print(f"📚 多页模板: {multi_page}")
    print("\n💡 这些PDF文件可以直接打印使用，适合小学生练习写字。")
    print("📝 每个方格大小为7mm x 7mm，每5个格子有粗线分隔，便于书写。")
