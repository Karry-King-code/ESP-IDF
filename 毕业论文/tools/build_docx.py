# -*- coding: utf-8 -*-
"""把 content/*.md 渲染成符合中文学位论文排版习惯的 .docx。

Markdown 方言（只支持本文件用到的子集）：
  # / ## / ###      一级（章）/二级/三级标题
  普通行            正文段落（首行缩进 2 字符、小四宋体、1.5 倍行距）
  - 项              无序列表
  | a | b |         表格（第一行为表头）
  [IMG:路径|宽cm|图题]
  [PAGEBREAK]
  [RIGHT]文本       右对齐文本（签名行等）
  [CENTER]文本      居中文本
  [BLANK]           空行

运行：python tools/build_docx.py
"""
import os
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
FIG = os.path.join(ROOT, "figures")

SONG = "宋体"
HEI = "黑体"
KAI = "楷体"
TIMES = "Times New Roman"


# ----------------------------------------------------------------- 基础排版工具
def set_run(run, name=SONG, size=12, bold=False, color=None):
    run.font.name = TIMES
    run.font.size = Pt(size)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), name)
    rfonts.set(qn("w:ascii"), TIMES)
    rfonts.set(qn("w:hAnsi"), TIMES)
    if color:
        run.font.color.rgb = RGBColor(*color)


def fmt_para(p, first_indent=0, before=0, after=0, line=1.5, align=None):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if first_indent:
        pf.first_line_indent = Pt(first_indent)
    if align is not None:
        p.alignment = align


def add_para(doc, text, size=12, name=SONG, bold=False, first_indent=24,
             before=0, after=0, line=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    fmt_para(p, first_indent, before, after, line, align)
    _rich(p, text, size, name, bold)
    return p


def _rich(p, text, size, name, bold):
    """支持 **加粗** 与 {{1}} / {{1,2}} 上标引用。"""
    for i, seg in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not seg:
            continue
        is_bold = bold or (i % 2 == 1)
        for j, part in enumerate(re.split(r"\{\{([\d,\-]+)\}\}", seg)):
            if not part:
                continue
            if j % 2 == 1:
                run = p.add_run("[" + part + "]")
                set_run(run, name, size, is_bold)
                run.font.superscript = True
            else:
                run = p.add_run(part)
                set_run(run, name, size, is_bold)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    if level == 1:
        fmt_para(p, 0, 18, 12, 1.5, WD_ALIGN_PARAGRAPH.LEFT)
        run = p.add_run(text)
        set_run(run, HEI, 16, True)
    elif level == 2:
        fmt_para(p, 0, 12, 6, 1.5, WD_ALIGN_PARAGRAPH.LEFT)
        run = p.add_run(text)
        set_run(run, HEI, 14, True)
    else:
        fmt_para(p, 0, 6, 3, 1.5, WD_ALIGN_PARAGRAPH.LEFT)
        run = p.add_run(text)
        set_run(run, HEI, 12, True)
    return p


def add_caption(doc, text, before=6, after=12):
    p = doc.add_paragraph()
    fmt_para(p, 0, before, after, 1.0, WD_ALIGN_PARAGRAPH.CENTER)
    run = p.add_run(text)
    set_run(run, SONG, 10.5, False)


def add_image(doc, path, width_cm):
    p = doc.add_paragraph()
    fmt_para(p, 0, 6, 0, 1.0, WD_ALIGN_PARAGRAPH.CENTER)
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))


def add_table(doc, rows, font_size=9.5, widths=None):
    cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=cols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    if widths:
        table.autofit = False
        _fixed_layout(table)
        for ci in range(cols):
            table.columns[ci].width = Cm(widths[ci] if ci < len(widths) else 3.0)
    else:
        table.autofit = True
    for ri, row in enumerate(rows):
        for ci in range(cols):
            cell = table.cell(ri, ci)
            cell.text = ""
            p = cell.paragraphs[0]
            fmt_para(p, 0, 2, 2, 1.0, WD_ALIGN_PARAGRAPH.CENTER)
            txt = row[ci] if ci < len(row) else ""
            run = p.add_run(txt)
            set_run(run, SONG, font_size, ri == 0)
            if widths and ci < len(widths):
                cell.width = Cm(widths[ci])
    return table


def add_page_number_footer(section):
    section.different_first_page_header_footer = True
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run(run, SONG, 10.5)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._element.addnext(fld)


def page_setup(doc):
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.top_margin, s.bottom_margin = Cm(2.54), Cm(2.54)
    s.left_margin, s.right_margin = Cm(3.0), Cm(2.6)


def new_doc():
    doc = Document()
    page_setup(doc)
    st = doc.styles["Normal"]
    st.font.name = TIMES
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), SONG)
    return doc


def pagebreak(doc):
    p = doc.add_paragraph()
    fmt_para(p, 0, 0, 0, 1.0)
    p.add_run().add_break(WD_BREAK.PAGE)


# ----------------------------------------------------------------- 封面
def cover(doc, kind, meta):
    if kind == "task":
        # 顶部单位名
        p = doc.add_paragraph()
        fmt_para(p, 0, 24, 6, 1.5, WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run("广州南方学院")
        set_run(r, HEI, 22, True)
        p = doc.add_paragraph()
        fmt_para(p, 0, 6, 30, 1.5, WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run("毕业论文（设计）任务书")
        set_run(r, HEI, 26, True)

        title = meta["title"]
        p = doc.add_paragraph()
        fmt_para(p, 0, 8, 2, 1.5, WD_ALIGN_PARAGRAPH.LEFT)
        r = p.add_run("毕业论文（设计）题目")
        set_run(r, HEI, 12, True)
        p = doc.add_paragraph()
        fmt_para(p, 0, 2, 14, 1.5, WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(title)
        set_run(r, HEI, 16, True)

        rows = [
            ("学生姓名", meta["name"], "学    号", meta["sid"]),
            ("学    院", meta["college"], "专    业", meta["major"]),
            ("指导教师", meta["teacher"], "职    称", meta["rank"]),
        ]
        table = doc.add_table(rows=len(rows), cols=4)
        table.autofit = False
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        widths = [Cm(3.0), Cm(4.1), Cm(2.7), Cm(5.6)]
        _fixed_layout(table)
        for ci in range(4):
            table.columns[ci].width = widths[ci]
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                cell = table.cell(ri, ci)
                cell.width = widths[ci]
                cell.text = ""
                p = cell.paragraphs[0]
                fmt_para(p, 0, 8, 8, 1.0, WD_ALIGN_PARAGRAPH.CENTER)
                r = p.add_run(val)
                set_run(r, HEI if ci % 2 == 0 else SONG, 12, ci % 2 == 0)
                _cell_bottom_border(cell)

        p = doc.add_paragraph()
        fmt_para(p, 0, 16, 0, 1.0, WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(meta["date"])
        set_run(r, SONG, 12)
        pagebreak(doc)
    else:
        # 开题报告封面
        for txt, size, before, after in (("本科生毕业论文（设计）", 18, 30, 24),
                                         ("开 题 报 告", 36, 24, 40)):
            p = doc.add_paragraph()
            fmt_para(p, 0, before, after, 1.5, WD_ALIGN_PARAGRAPH.CENTER)
            r = p.add_run(txt)
            set_run(r, HEI if size < 30 else HEI, size, True)

        items = [
            ("题目", meta["title"]),
            ("学院", meta["college"]),
            ("专业", meta["major"]),
            ("学生姓名", meta["name"]),
            ("学号", meta["sid"]),
            ("指导教师", meta["teacher"]),
        ]
        table = doc.add_table(rows=len(items), cols=2)
        table.autofit = False
        _fixed_layout(table)
        table.columns[0].width = Cm(4.4)
        table.columns[1].width = Cm(10.6)
        for ri, (label, val) in enumerate(items):
            for ci, (txt, align) in enumerate(((label + "：", WD_ALIGN_PARAGRAPH.RIGHT),
                                               (val, WD_ALIGN_PARAGRAPH.LEFT))):
                cell = table.cell(ri, ci)
                cell.width = Cm(4.4 if ci == 0 else 10.6)
                cell.text = ""
                p = cell.paragraphs[0]
                fmt_para(p, 0, 8, 8, 1.5, align)
                r = p.add_run(txt)
                set_run(r, SONG, 14, False)
                _cell_bottom_border(cell, none=True)

        p = doc.add_paragraph()
        fmt_para(p, 0, 40, 0, 1.5, WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(meta["date"])
        set_run(r, HEI, 14)
        pagebreak(doc)


def _fixed_layout(table):
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)


def _cell_bottom_border(cell, none=False):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "right", "bottom"):
        el = OxmlElement(f"w:{edge}")
        if none:
            el.set(qn("w:val"), "nil")
        elif edge == "bottom":
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), "8")
            el.set(qn("w:color"), "000000")
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)
    tcPr.append(borders)


# ----------------------------------------------------------------- Markdown 渲染
def render_md(doc, md_text):
    lines = md_text.splitlines()
    i = 0
    pending_w = None
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        i += 1

        if not line:
            continue
        if line.startswith("[TW:"):
            pending_w = [float(x) for x in line[4:-1].split(",")]
            continue
        if line.startswith("[TCAP:"):
            add_caption(doc, line[6:-1].strip(), before=6, after=2)
            continue
        if line.startswith("[SIGN:"):
            label, date = line[6:-1].split("|", 1)
            t = doc.add_table(rows=1, cols=2)
            t.alignment = WD_TABLE_ALIGNMENT.RIGHT
            t.autofit = False
            _fixed_layout(t)
            t.columns[0].width = Cm(6.4)
            t.columns[1].width = Cm(6.0)
            for ci, (txt, al) in enumerate(((label.strip(), WD_ALIGN_PARAGRAPH.RIGHT),
                                            (date.strip(), WD_ALIGN_PARAGRAPH.CENTER))):
                cell = t.cell(0, ci)
                cell.width = Cm(6.4 if ci == 0 else 6.0)
                cell.text = ""
                p = cell.paragraphs[0]
                fmt_para(p, 0, 6, 6, 1.5, al)
                r = p.add_run(txt)
                set_run(r, SONG, 12)
                _cell_bottom_border(cell, none=True)
            continue
        if line.startswith("[PAGEBREAK]"):
            pagebreak(doc)
            continue
        if line.startswith("[BLANK]"):
            p = doc.add_paragraph()
            fmt_para(p, 0, 0, 0, 1.0)
            continue
        if line.startswith("[IMG:"):
            body = line[5:-1]
            path, rest = body.split("|", 1)
            width, capt = rest.split("|", 1)
            add_image(doc, os.path.join(ROOT, path.strip()), float(width))
            add_caption(doc, capt.strip())
            continue
        if line.startswith("[RIGHT]"):
            add_para(doc, line[7:].strip(), first_indent=0,
                     align=WD_ALIGN_PARAGRAPH.RIGHT)
            continue
        if line.startswith("[CENTER]"):
            add_para(doc, line[8:].strip(), first_indent=0,
                     align=WD_ALIGN_PARAGRAPH.CENTER)
            continue
        if line.startswith("### "):
            add_heading(doc, line[4:].strip(), 3)
            continue
        if line.startswith("## "):
            add_heading(doc, line[3:].strip(), 2)
            continue
        if line.startswith("# "):
            add_heading(doc, line[2:].strip(), 1)
            continue
        if line.startswith("|"):
            rows = []
            while i <= len(lines) and lines[i - 1].strip().startswith("|"):
                cur = lines[i - 1].strip()
                cells = [c.strip() for c in cur.strip("|").split("|")]
                if not re.fullmatch(r"[-\s:|]+", cur.replace("|", "")):
                    rows.append(cells)
                i += 1
            add_table(doc, rows, widths=pending_w)
            pending_w = None
            p = doc.add_paragraph()
            fmt_para(p, 0, 0, 6, 1.0)
            continue
        if re.match(r"^\[\d+\]", line):
            p = add_para(doc, line, size=10.5, first_indent=0, line=1.25,
                         align=WD_ALIGN_PARAGRAPH.LEFT)
            p.paragraph_format.left_indent = Pt(0)
            continue
        if line.startswith("- "):
            items = []
            while i <= len(lines) and lines[i - 1].strip().startswith("- "):
                items.append(lines[i - 1].strip()[2:])
                i += 1
            for it in items:
                p = doc.add_paragraph()
                fmt_para(p, 24, 0, 0, 1.5, WD_ALIGN_PARAGRAPH.JUSTIFY)
                p.paragraph_format.left_indent = Pt(0)
                _rich(p, "· " + it, 12, SONG, False)
            continue
        add_para(doc, line)


def build(md_name, docx_name, kind, meta, footer=True):
    doc = new_doc()
    if footer:
        add_page_number_footer(doc.sections[0])
    cover(doc, kind, meta)
    with open(os.path.join(CONTENT, md_name), encoding="utf-8") as f:
        render_md(doc, f.read())
    out = os.path.join(ROOT, docx_name)
    doc.save(out)
    print("saved", docx_name)


META = {
    "title": "基于ESP32-S3的智能终端设计与实现",
    "name": "姚凯锐",
    "sid": "2320158058",
    "college": "工学院",
    "major": "电气工程及其自动化",
    "teacher": "曹春妍",
    "rank": "副教授",
    "date": "2026年10月30日",
}
META2 = dict(META, date="2026年11月16日")

if __name__ == "__main__":
    build("taskbook.md", "1.2320158058_姚凯锐_任务书.docx", "task", META)
    build("proposal.md", "2.2320158058_姚凯锐_开题报告.docx", "proposal", META2)
