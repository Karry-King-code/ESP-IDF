# -*- coding: utf-8 -*-
"""生成开题报告 / 任务书所需的插图（纯 PIL 绘制，无外部依赖）。

设计原则：画布宽 2000px 对应 Word 中约 15 cm 的排版宽度，
因此图中 32~36px 的文字约等于 7.5~8.5 磅，保证打印后可读。
运行：python tools/figs.py
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
        ("人机交互", ["LVGL 界面", "触摸与按键", "桌面与 APP"]),
        ("网络通信", ["WiFi 联网", "天气获取", "时间与日历"]),
        ("多媒体", ["音乐播放", "I2S 功放", "AI 语音"]),
        ("感知控制", ["电池采样", "RGB 灯效", "呼吸灯"]),
        ("系统调试", ["串口终端", "参数存储", "设置 / 关于"]),
        ("娱乐扩展", ["LVGL 游戏", "触摸适配", "OTA 扩展"]),
    ]
    W = 2000
    col_w, gap = 300, 32
    left = (W - (col_w * len(groups) + gap * (len(groups) - 1))) / 2
    centers = [left + col_w / 2 + i * (col_w + gap) for i in range(len(groups))]

    rw, rh, ry = 780, 120, 36
    bus_y = ry + rh + 56
    gy, gh = bus_y + 36, 100
    leaf_top, leaf_h, leaf_gap = gy + gh + 34, 84, 26
    bottom = leaf_top + 3 * leaf_h + 2 * leaf_gap
    H = int(bottom + 30)

    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    box(dr, (W - rw) / 2, ry, rw, rh, fill=DARK, outline=DARK, r=16)
    text(dr, W / 2, ry + rh / 2, "ESP32-S3 智能终端系统", font(46, True), WHITE)

    dr.line([W / 2, ry + rh, W / 2, bus_y], fill=MAIN, width=4)
    dr.line([centers[0], bus_y, centers[-1], bus_y], fill=MAIN, width=4)

    for cx, (gname, leaves) in zip(centers, groups):
        dr.line([cx, bus_y, cx, gy], fill=MAIN, width=4)
        box(dr, cx - col_w / 2, gy, col_w, gh, fill=LIGHT, outline=MAIN, r=14)
        text(dr, cx, gy + gh / 2, gname, font(36, True), DARK)

        ly = leaf_top
        for leaf in leaves:
            lw = col_w - 18
            dr.line([cx, ly - 34, cx, ly], fill=SOFT, width=3)
            box(dr, cx - lw / 2, ly, lw, leaf_h, fill=PALE, outline=LEAF_EDGE, r=12)
            text(dr, cx, ly + leaf_h / 2, leaf, font(32), INK)
            ly += leaf_h + leaf_gap

    im.save(os.path.join(OUT, "fig_function.png"), dpi=(220, 220))


# ---------------------------------------------------------------- 开发思维导图
def fig_roadmap():
    steps = [
        ("需求分析与功能定义", "终端定位、功能清单、性能与成本指标", "第 1 阶段"),
        ("硬件原理图与引脚规划", "ESP32-S3 资源分配、外设接口与电平极性", "第 1—2 阶段"),
        ("ESP-IDF 开发环境搭建", "VSCode + ESP-IDF、工程骨架与组件划分", "第 2—3 阶段"),
        ("底层驱动开发", "GPIO / LEDC / 定时器 / ADC / UART / SPI", "第 3—4 阶段"),
        ("显示与触摸子系统", "ST7789 屏驱动、XPT2046 坐标标定", "第 4 阶段"),
        ("LVGL 图形框架移植", "显示缓冲、刷新机制、颜色字节序", "第 4 阶段"),
        ("UI 设计与事件机制", "页面布局、控件样式、事件回调", "第 5 阶段"),
        ("FreeRTOS 多任务划分", "任务优先级、队列通信、栈与内存规划", "第 5 阶段"),
        ("联网与信息服务", "WiFi 配网、HTTP 天气、SNTP 校时", "第 5—6 阶段"),
        ("音频链路（录放音）", "SD 卡 FATFS、I2S 功放、麦克风采集", "第 6 阶段"),
        ("系统联调与测试", "功能测试、稳定性与续航测试、缺陷闭环", "第 6—7 阶段"),
        ("优化、文档与答辩", "性能优化、论文撰写、材料归档", "第 7—8 阶段"),
    ]
    W = 2000
    top, row = 54, 118
    box_x, box_w, box_h = 200, 1430, 100
    H = int(top + (len(steps) - 1) * row + box_h / 2 + 26)
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    for i, (title, detail, phase) in enumerate(steps):
        cy = top + i * row
        if i < len(steps) - 1:
            dr.line([124, cy + 24, 124, cy + row - 24], fill=SOFT, width=4)
        dr.ellipse([100, cy - 24, 148, cy + 24], fill=MAIN)
        text(dr, 124, cy, str(i + 1), font(26, True), WHITE)

        box(dr, box_x, cy - box_h / 2, box_w, box_h, fill=LIGHT, outline=MAIN, r=14)
        text_left(dr, box_x + 28, cy - 22, title, font(31, True), DARK)
        text_left(dr, box_x + 28, cy + 24, detail, font(26), GREY)

        pw = 180
        box(dr, W - 56 - pw, cy - 28, pw, 56, fill=WHITE, outline=LEAF_EDGE, r=28)
        text(dr, W - 56 - pw / 2, cy, phase, font(24), MAIN)

    im.save(os.path.join(OUT, "fig_roadmap.png"), dpi=(220, 220))


# ---------------------------------------------------------------- 总体架构
def fig_arch():
    layers = [
        ("应用层", ["桌面", "设置", "天气日历", "音乐", "AI 语音", "串口", "游戏", "关于"],
         (226, 240, 217), (84, 140, 55)),
        ("中间件层", ["LVGL v9", "FreeRTOS", "FATFS", "lwIP", "NVS", "音频解码"],
         (222, 235, 247), (46, 117, 182)),
        ("驱动层", ["lcd / touch", "lvgl / ui", "rgb / key", "adc / timer", "uart / wifi",
                "music / 语音"],
         (255, 242, 204), (168, 124, 0)),
        ("硬件层", ["ESP32-S3", "ST7789 屏", "XPT2046", "NS4168", "PDM 麦克风",
                "Micro SD", "RGB / 按键", "TP4056"],
         (237, 226, 240), (112, 48, 160)),
    ]
    W, label_w, pad = 2000, 250, 22
    y, gap_v, inner_h = 40, 50, 156
    H = int(y + len(layers) * inner_h + (len(layers) - 1) * gap_v + 24)
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    for idx, (name, items, fill, edge) in enumerate(layers):
        box(dr, 40, y, W - 80, inner_h, fill=fill, outline=edge, r=16)
        text(dr, 40 + label_w / 2 - 12, y + inner_h / 2, name, font(32, True), edge)

        n = len(items)
        avail = W - 80 - label_w - pad
        iw = (avail - pad * (n - 1)) / n
        fnt = font(28 if n >= 8 else 30, True)
        for i, it in enumerate(items):
            x = 40 + label_w + i * (iw + pad)
            box(dr, x, y + 26, iw, inner_h - 52, fill=WHITE, outline=edge, r=10, width=2)
            text(dr, x + iw / 2, y + inner_h / 2, it, fnt, INK, spacing=4)

        if idx < len(layers) - 1:
            cx = W / 2 + 120
            arrow(dr, cx, y + inner_h + 5, cx, y + inner_h + gap_v - 5, MAIN, 4, both=True)

        y += inner_h + gap_v

    im.save(os.path.join(OUT, "fig_arch.png"), dpi=(220, 220))


# ---------------------------------------------------------------- 阶段进度
def fig_schedule():
    phases = [
        ("第 1 阶段", "需求分析", "8.01—8.31"),
        ("第 2 阶段", "系统设计", "9.01—9.14"),
        ("第 3 阶段", "环境搭建\n原型设计", "9.15—9.30"),
        ("第 4 阶段", "驱动与界面", "10.01—10.31"),
        ("第 5 阶段", "应用功能", "11.01—11.30"),
        ("第 6 阶段", "集成测试", "12.01—12.10"),
        ("第 7 阶段", "修复优化", "12.11—12.15"),
        ("第 8 阶段", "发布答辩", "12.16—12.20"),
    ]
    W, H = 2000, 620
    im = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(im)

    n = len(phases)
    left, right = 210, W - 210
    axis_y = 330
    dr.line([left - 50, axis_y, right + 50, axis_y], fill=(180, 195, 215), width=5)
    step = (right - left) / (n - 1)

    for i, (p, name, date) in enumerate(phases):
        cx = left + i * step
        up = i % 2 == 0
        w, h = 236, 132
        if up:
            by = axis_y - 44 - h
            dr.line([cx, by + h, cx, axis_y - 18], fill=SOFT, width=4)
            dy = by - 30
        else:
            by = axis_y + 44
            dr.line([cx, axis_y + 18, cx, by], fill=SOFT, width=4)
            dy = by + h + 30
        dr.ellipse([cx - 16, axis_y - 16, cx + 16, axis_y + 16], fill=WHITE, outline=MAIN, width=5)
        box(dr, cx - w / 2, by, w, h, fill=LIGHT, outline=MAIN, r=14)
        text(dr, cx, by + 30, p, font(27, True), MAIN)
        text(dr, cx, by + h * 0.64, name, font(31, True), DARK, spacing=4)
        text(dr, cx, dy, date, font(26), GREY)

    im.save(os.path.join(OUT, "fig_schedule.png"), dpi=(220, 220))


if __name__ == "__main__":
    fig_function()
    fig_roadmap()
    fig_arch()
    fig_schedule()
    print("done ->", OUT)
    for f in sorted(os.listdir(OUT)):
        print("  ", f, os.path.getsize(os.path.join(OUT, f)) // 1024, "KB")
