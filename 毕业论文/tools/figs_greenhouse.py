# -*- coding: utf-8 -*-
"""农业大棚项目的插图（画布宽 2000px ≈ Word 中 15 cm 排版宽度）。

运行：python tools/figs_greenhouse.py
输出：figures/gh_*.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "figures")
os.makedirs(OUT, exist_ok=True)

FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
if not os.path.exists(FONT_BOLD):
    FONT_BOLD = FONT_REG

INK = (31, 31, 31)
DARK = (31, 78, 121)
MAIN = (46, 117, 182)
GREEN = (56, 118, 61)
GREEN_FILL = (226, 240, 217)
GREEN_EDGE = (84, 140, 55)
ORANGE = (168, 100, 0)
ORANGE_FILL = (255, 242, 204)
PURPLE = (112, 48, 160)
PURPLE_FILL = (237, 226, 240)
LIGHT = (222, 235, 247)
PALE = (244, 249, 254)
WHITE = (255, 255, 255)
GREY = (105, 118, 132)
SOFT = (150, 175, 205)
LEAF_EDGE = (142, 170, 219)


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def box(dr, x, y, w, h, fill=LIGHT, outline=MAIN, r=12, width=2):
    dr.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill,
                         outline=outline, width=width)


def tsize(dr, s, fnt):
    b = dr.textbbox((0, 0), s, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def text(dr, cx, cy, s, fnt, fill=INK, spacing=6):
    lines = s.split("\n")
    lh = tsize(dr, "测", fnt)[1] + spacing
    total = lh * len(lines) - spacing
    y = cy - total / 2 + lh / 2
    for ln in lines:
        dr.text((cx, y), ln, font=fnt, fill=fill, anchor="mm")
        y += lh


def text_left(dr, x, cy, s, fnt, fill=INK):
    dr.text((x, cy), s, font=fnt, fill=fill, anchor="lm")


def arrow(dr, x1, y1, x2, y2, color=MAIN, width=4, head=14, both=False):
    dr.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (+1, -1):
        a = ang + s * 0.42
        dr.line([x2, y2, x2 - head * math.cos(a), y2 - head * math.sin(a)],
                fill=color, width=width)
    if both:
        ang2 = ang + math.pi
        for s in (+1, -1):
            a = ang2 + s * 0.42
            dr.line([x1, y1, x1 - head * math.cos(a), y1 - head * math.sin(a)],
                    fill=color, width=width)


# ---------------------------------------------------------------- 功能结构图
def fig_function():
    groups = [
        ("环境采集", ["空气温湿度", "CO2 浓度", "光照强度"]),
        ("土壤监测", ["土壤湿度", "土壤 pH 值", "数据校准"]),
        ("自动控制", ["通风降温", "雾化加湿", "灌溉水泵"]),
        ("本地交互", ["OLED 显示", "按键设置", "声光报警"]),
        ("远程通信", ["WiFi 联网", "手机 APP", "云平台"]),
        ("系统管理", ["自动/手动", "阈值设定", "参数存储"]),
    ]
    W = 2000
    col_w, gap = 300, 32
    left = (W - (col_w * len(groups) + gap * (len(groups) - 1))) / 2
    centers = [left + col_w / 2 + i * (col_w + gap) for i in range(len(groups))]

    rw, rh, ry = 820, 120, 36
    bus_y = ry + rh + 56
    gy, gh = bus_y + 36, 100
    leaf_top, leaf_h, leaf_gap = gy + gh + 34, 84, 26
    bottom = leaf_top + 3 * leaf_h + 2 * leaf_gap
    H = int(bottom + 30)

    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    box(dr, (W - rw) / 2, ry, rw, rh, fill=GREEN, outline=GREEN, r=16)
    text(dr, W / 2, ry + rh / 2, "农业大棚环境检测与远程控制系统", font(42, True), WHITE)

    dr.line([W / 2, ry + rh, W / 2, bus_y], fill=GREEN_EDGE, width=4)
    dr.line([centers[0], bus_y, centers[-1], bus_y], fill=GREEN_EDGE, width=4)

    for cx, (gname, leaves) in zip(centers, groups):
        dr.line([cx, bus_y, cx, gy], fill=GREEN_EDGE, width=4)
        box(dr, cx - col_w / 2, gy, col_w, gh, fill=GREEN_FILL, outline=GREEN_EDGE, r=14)
        text(dr, cx, gy + gh / 2, gname, font(34, True), GREEN)

        ly = leaf_top
        for leaf in leaves:
            lw = col_w - 18
            dr.line([cx, ly - 34, cx, ly], fill=(150, 175, 205), width=3)
            box(dr, cx - lw / 2, ly, lw, leaf_h, fill=PALE, outline=LEAF_EDGE, r=12)
            text(dr, cx, ly + leaf_h / 2, leaf, font(30), INK)
            ly += leaf_h + leaf_gap

    im.save(os.path.join(OUT, "gh_function.png"), dpi=(220, 220))


# ---------------------------------------------------------------- 总体架构
def fig_arch():
    layers = [
        ("感知层", ["DHT11\n温湿度", "SGP30\nCO2", "GL5506\n光照", "YL-69\n土壤湿度", "pH 传感器"],
         GREEN_FILL, GREEN_EDGE),
        ("控制层", ["STM32F103\nC8T6 主控", "最小系统\n时钟·复位", "电源模块\n5V / 3.3V",
                 "调试接口\nSWD"],
         LIGHT, MAIN),
        ("执行层", ["继电器 1\n风扇", "继电器 2\n加湿器", "继电器 3\n水泵", "LED\n补光灯", "有源\n蜂鸣器"],
         ORANGE_FILL, ORANGE),
        ("交互与通信", ["0.96 寸\nOLED", "独立按键", "ESP8266\nWiFi", "手机 APP", "云平台"],
         PURPLE_FILL, PURPLE),
    ]
    W, label_w, pad = 2000, 250, 22
    y, gap_v, inner_h = 40, 50, 156
    H = int(y + len(layers) * inner_h + (len(layers) - 1) * gap_v + 24)
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    for idx, (name, items, fill, edge) in enumerate(layers):
        box(dr, 40, y, W - 80, inner_h, fill=fill, outline=edge, r=16)
        text(dr, 40 + label_w / 2 - 12, y + inner_h / 2, name, font(31, True), edge)

        n = len(items)
        avail = W - 80 - label_w - pad
        iw = (avail - pad * (n - 1)) / n
        for i, it in enumerate(items):
            x = 40 + label_w + i * (iw + pad)
            box(dr, x, y + 26, iw, inner_h - 52, fill=WHITE, outline=edge, r=10, width=2)
            text(dr, x + iw / 2, y + inner_h / 2, it, font(26, True), INK, spacing=2)

        if idx < len(layers) - 1:
            cx = W / 2 + 120
            arrow(dr, cx, y + inner_h + 5, cx, y + inner_h + gap_v - 5, MAIN, 4, both=True)

        y += inner_h + gap_v

    im.save(os.path.join(OUT, "gh_arch.png"), dpi=(220, 220))


# ---------------------------------------------------------------- 技术路线
def fig_roadmap():
    steps = [
        ("研究背景与需求分析", "设施农业痛点、功能与非功能需求", "第 1 阶段"),
        ("系统总体方案设计", "模块划分、总体结构框图、工作流程", "第 1—2 阶段"),
        ("硬件选型与电路设计", "主控、传感器、执行机构、通信模块选型", "第 2—3 阶段"),
        ("最小系统与传感器调试", "STM32 最小系统、DHT11 / SGP30 通信验证", "第 3 阶段"),
        ("执行与报警电路设计", "继电器隔离驱动、蜂鸣器报警、补光灯", "第 3—4 阶段"),
        ("显示与按键交互", "OLED 显示界面、按键阈值设置与消抖", "第 4 阶段"),
        ("通信链路开发", "ESP8266 联网、APP 数据上传与指令下发", "第 4—5 阶段"),
        ("控制策略与双模式", "阈值判断、自动/手动切换、闭环调节", "第 5 阶段"),
        ("软硬件联调", "整机联调、传感器校准、异常处理", "第 5—6 阶段"),
        ("系统测试与优化", "功能测试、稳定性与精度测试、缺陷修复", "第 6—7 阶段"),
        ("论文撰写与答辩准备", "数据整理、论文成稿、演示材料", "第 7—8 阶段"),
    ]
    W = 2000
    top, row = 54, 122
    box_x, box_w, box_h = 200, 1430, 104
    H = int(top + (len(steps) - 1) * row + box_h / 2 + 26)
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    for i, (title, detail, phase) in enumerate(steps):
        cy = top + i * row
        if i < len(steps) - 1:
            dr.line([124, cy + 24, 124, cy + row - 24], fill=SOFT, width=4)
        dr.ellipse([100, cy - 24, 148, cy + 24], fill=GREEN, outline=GREEN)
        text(dr, 124, cy, str(i + 1), font(25, True), WHITE)

        box(dr, box_x, cy - box_h / 2, box_w, box_h, fill=GREEN_FILL, outline=GREEN_EDGE, r=14)
        text_left(dr, box_x + 28, cy - 23, title, font(31, True), GREEN)
        text_left(dr, box_x + 28, cy + 25, detail, font(25), GREY)

        pw = 180
        box(dr, W - 56 - pw, cy - 28, pw, 56, fill=WHITE, outline=LEAF_EDGE, r=28)
        text(dr, W - 56 - pw / 2, cy, phase, font(23), GREEN_EDGE)

    im.save(os.path.join(OUT, "gh_roadmap.png"), dpi=(220, 220))


if __name__ == "__main__":
    fig_function()
    fig_arch()
    fig_roadmap()
    print("done ->", OUT)
