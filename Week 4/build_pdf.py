from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

doc = SimpleDocTemplate(
    "/home/claude/week4/theory/Week4_Theory_TSP_Hamiltonian.pdf",
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=26,
    textColor=colors.HexColor('#1a1a2e'),
    spaceAfter=6,
    fontName='Helvetica-Bold',
    alignment=TA_CENTER,
)
subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=13,
    textColor=colors.HexColor('#4a4a8a'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Oblique',
)
h1_style = ParagraphStyle(
    'H1',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#1a1a2e'),
    spaceBefore=18,
    spaceAfter=6,
    fontName='Helvetica-Bold',
    borderPad=4,
)
h2_style = ParagraphStyle(
    'H2',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2d4070'),
    spaceBefore=12,
    spaceAfter=4,
    fontName='Helvetica-Bold',
)
body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#222222'),
    spaceAfter=8,
    leading=17,
    alignment=TA_JUSTIFY,
    fontName='Helvetica',
)
code_style = ParagraphStyle(
    'Code',
    parent=styles['Normal'],
    fontSize=9.5,
    textColor=colors.HexColor('#1a1a2e'),
    backColor=colors.HexColor('#f0f0f8'),
    fontName='Courier',
    leftIndent=12,
    rightIndent=12,
    spaceBefore=6,
    spaceAfter=6,
    leading=14,
    borderPad=6,
)
note_style = ParagraphStyle(
    'Note',
    parent=styles['Normal'],
    fontSize=10.5,
    textColor=colors.HexColor('#1a3a1a'),
    backColor=colors.HexColor('#e8f5e8'),
    fontName='Helvetica-Oblique',
    leftIndent=10,
    rightIndent=10,
    spaceBefore=6,
    spaceAfter=6,
    leading=15,
    borderPad=8,
)
warning_style = ParagraphStyle(
    'Warning',
    parent=styles['Normal'],
    fontSize=10.5,
    textColor=colors.HexColor('#3a1a00'),
    backColor=colors.HexColor('#fff3e0'),
    fontName='Helvetica',
    leftIndent=10,
    rightIndent=10,
    spaceBefore=6,
    spaceAfter=6,
    leading=15,
    borderPad=8,
)
bullet_style = ParagraphStyle(
    'BulletItem',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#222222'),
    leftIndent=20,
    spaceAfter=4,
    leading=16,
    bulletIndent=8,
)

def hr():
    return HRFlowable(width="100%", thickness=1.2, color=colors.HexColor('#c0c8e0'), spaceAfter=8, spaceBefore=4)

def section_box(text, bg=colors.HexColor('#eef0fb')):
    # Split into lines and create a paragraph per line to avoid XML parsing issues
    lines = text.split('\n')
    sb_style = ParagraphStyle('SB', parent=styles['Normal'], fontSize=10.5,
                              textColor=colors.HexColor('#1a1a2e'), fontName='Courier',
                              leading=15, spaceAfter=0, spaceBefore=0)
    def safe(s):
        if not s.strip():
            return '&nbsp;'
        return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    paras = [Paragraph(safe(line), sb_style) for line in lines]
    data = [[p] for p in paras]
    t = Table(data, colWidths=[16.5*cm])
    cmd = [
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#b0b8d8')),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (0,0), 8),
        ('BOTTOMPADDING', (-1,-1), (-1,-1), 8),
        ('TOPPADDING', (0,1), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-2), 1),
    ]
    t.setStyle(TableStyle(cmd))
    return t

story = []

# ── COVER ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("Week 4: K Shortest Paths &amp;", title_style))
story.append(Paragraph("TSP Consolidation", title_style))
story.append(Paragraph("Theory Guide — Hamiltonian Cycles &amp; Travelling Salesman Problem", subtitle_style))
story.append(hr())
story.append(Spacer(1, 0.4*cm))

meta_data = [
    ["Module", "Week 4 — Graph Algorithms"],
    ["Topics", "Graph Recap · Hamiltonian Cycle · TSP · Complexity"],
    ["Prereqs", "Basic graph theory, DFS/BFS, Dijkstra's algorithm"],
    ["Level", "Intermediate / Pre-competitive"],
]
meta_table = Table(meta_data, colWidths=[4*cm, 12.5*cm])
meta_table.setStyle(TableStyle([
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10.5),
    ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor('#333333')),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#c0c8e0')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
]))
story.append(meta_table)
story.append(Spacer(1, 0.8*cm))

# ── SECTION 1: QUICK GRAPH RECAP ───────────────────────────────────────────────
story.append(Paragraph("1. Quick Graph Recap", h1_style))
story.append(hr())
story.append(Paragraph(
    "Before diving into Hamiltonian cycles and TSP, make sure the following vocabulary is rock-solid. "
    "These ideas will appear constantly in competitive programming.",
    body_style))

concepts = [
    ["Term", "Definition", "Example"],
    ["Vertex (node)", "A point/city in the graph", "City A, City B …"],
    ["Edge", "A connection between two vertices", "Road from A to B"],
    ["Weight", "Cost/distance assigned to an edge", "Distance = 42 km"],
    ["Degree", "Number of edges touching a vertex", "City A has 3 roads"],
    ["Path", "A sequence of vertices connected by edges (no repeated vertex)", "A → B → C → D"],
    ["Cycle", "A path that starts and ends at the same vertex", "A → B → C → A"],
    ["Complete graph K_n", "Every pair of vertices is connected", "K_4 has 6 edges"],
    ["Connected graph", "There is a path between every pair of vertices", "All cities reachable"],
]
t = Table(concepts, colWidths=[3.8*cm, 8*cm, 4.7*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

# ── SECTION 2: HAMILTONIAN CYCLE ───────────────────────────────────────────────
story.append(Paragraph("2. Hamiltonian Cycle", h1_style))
story.append(hr())

story.append(Paragraph("2.1 Formal Definition", h2_style))
story.append(Paragraph(
    "A <b>Hamiltonian cycle</b> (also called a Hamiltonian circuit) in a graph G = (V, E) is a cycle that "
    "<b>visits every vertex exactly once</b> and returns to the starting vertex.",
    body_style))

story.append(section_box(
    "Definition — Hamiltonian Cycle:\n"
    "Given a graph G with n vertices, a Hamiltonian cycle is a sequence\n"
    "  v0, v1, v2, ..., v(n-1), v0\n"
    "such that:\n"
    "  (1)  Each vi is a distinct vertex of G\n"
    "  (2)  Each consecutive pair (vi, v(i+1)) is an edge in E\n"
    "  (3)  The pair (v(n-1), v0) is also an edge in E  (closing the cycle)"
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("2.2 Hamiltonian Path vs. Hamiltonian Cycle", h2_style))
story.append(Paragraph(
    "It is important to distinguish between a <b>Hamiltonian path</b> (visits every vertex exactly once, "
    "but does NOT need to return to start) and a <b>Hamiltonian cycle</b> (must return to start).",
    body_style))

diff_data = [
    ["Property", "Hamiltonian Path", "Hamiltonian Cycle"],
    ["Visits all vertices?", "Yes", "Yes"],
    ["Returns to start?", "No", "Yes"],
    ["Edges used", "n - 1", "n"],
    ["Application", "Route planning (one-way)", "TSP, circular routes"],
]
dt = Table(diff_data, colWidths=[4.5*cm, 6*cm, 6*cm])
dt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('ALIGN', (1,0), (-1,-1), 'CENTER'),
]))
story.append(dt)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("2.3 Does a Hamiltonian Cycle Always Exist?", h2_style))
story.append(Paragraph(
    "No! Not every graph has a Hamiltonian cycle. Deciding whether one exists is itself an NP-complete problem. "
    "However, some useful sufficient conditions exist:",
    body_style))

story.append(Paragraph(
    "<b>Dirac's Theorem (1952):</b> If every vertex in a simple graph with n >= 3 vertices has degree &gt;= n/2, "
    "then the graph has a Hamiltonian cycle.",
    bullet_style))
story.append(Paragraph(
    "<b>Ore's Theorem (1960):</b> If for every pair of non-adjacent vertices u, v we have "
    "deg(u) + deg(v) >= n, then the graph has a Hamiltonian cycle.",
    bullet_style))
story.append(Paragraph(
    "<b>Complete graphs K_n (n &gt;= 3):</b> Always have a Hamiltonian cycle.",
    bullet_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "<b>Small example:</b> Consider K_4 (4 cities: A, B, C, D). One Hamiltonian cycle: A → B → C → D → A. "
    "Another valid one: A → C → B → D → A. (These are considered the same cycle traversed differently.)",
    note_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("2.4 Counting Hamiltonian Cycles", h2_style))
story.append(Paragraph(
    "For a complete graph K_n, the number of distinct Hamiltonian cycles is:",
    body_style))
story.append(section_box("Number of Hamiltonian cycles in K_n  =  (n - 1)! / 2"))
story.append(Paragraph(
    "For n = 4 cities: (4-1)!/2 = 6/2 = 3 cycles. For n = 10: 9!/2 = 181,440 cycles. "
    "For n = 20: 19!/2 ≈ 60 trillion cycles. This explosive growth is exactly why brute force doesn't scale!",
    body_style))

story.append(PageBreak())

# ── SECTION 3: TSP ─────────────────────────────────────────────────────────────
story.append(Paragraph("3. The Travelling Salesman Problem (TSP)", h1_style))
story.append(hr())

story.append(Paragraph("3.1 Problem Statement", h2_style))
story.append(section_box(
    "TSP — Formal Statement:\n"
    "Given a complete weighted graph G = (V, E, w) where w(u,v) is the cost of edge (u,v),\n"
    "find a Hamiltonian cycle of minimum total weight.\n\n"
    "Input:  n cities, pairwise distances d[i][j]\n"
    "Output: A permutation of cities (a tour) that visits each city exactly once\n"
    "        and returns to start, minimising the total travel cost."
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "TSP is one of the most famous and extensively studied problems in computer science, operations research, "
    "and combinatorial optimisation. It has direct real-world applications in logistics, chip manufacturing, "
    "DNA sequencing, and more.",
    body_style))

story.append(Paragraph("3.2 Variants of TSP", h2_style))
variants = [
    ["Variant", "Key Constraint", "Notes"],
    ["Symmetric TSP", "d[i][j] = d[j][i]  for all i, j", "Most common; undirected graph"],
    ["Asymmetric TSP", "d[i][j] may ≠ d[j][i]", "Directed graph (one-way roads)"],
    ["Metric TSP", "Triangle inequality holds:\nd[i][k] ≤ d[i][j] + d[j][k]", "Allows approximation guarantees"],
    ["Euclidean TSP", "Cities are points in 2-D plane;\ndistance = straight-line", "Special metric TSP"],
]
vt = Table(variants, colWidths=[4*cm, 7*cm, 5.5*cm])
vt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(vt)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("3.3 A Worked Example (n = 4)", h2_style))
story.append(Paragraph(
    "Cities: 0 (Home), 1 (A), 2 (B), 3 (C). Distance matrix:",
    body_style))

dist_data = [
    ["", "0", "1", "2", "3"],
    ["0", "0", "10", "15", "20"],
    ["1", "10", "0", "35", "25"],
    ["2", "15", "35", "0", "30"],
    ["3", "20", "25", "30", "0"],
]
ddt = Table(dist_data, colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
ddt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('TEXTCOLOR', (0,0), (0,-1), colors.white),
    ('FONTNAME', (0,0), (-1,-1), 'Courier-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 11),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (1,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(ddt)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("All possible tours starting from city 0:", body_style))
tours_data = [
    ["Tour", "Cost Calculation", "Total"],
    ["0→1→2→3→0", "10 + 35 + 30 + 20", "95"],
    ["0→1→3→2→0", "10 + 25 + 30 + 15", "80  ← OPTIMAL"],
    ["0→2→1→3→0", "15 + 35 + 25 + 20", "95"],
]
tt = Table(tours_data, colWidths=[4.5*cm, 8*cm, 4*cm])
tt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Courier'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#d4edda')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(tt)
story.append(Spacer(1, 0.5*cm))

# ── SECTION 4: COMPLEXITY ──────────────────────────────────────────────────────
story.append(Paragraph("4. Why is TSP Hard? NP-Hardness", h1_style))
story.append(hr())

story.append(Paragraph("4.1 Brute Force — The Naive Approach", h2_style))
story.append(Paragraph(
    "The simplest algorithm tries every possible permutation of cities:",
    body_style))

story.append(Paragraph("Algorithm — Brute Force TSP:", code_style))
story.append(Paragraph(
    "1. Fix starting city (say city 0)\n"
    "2. Generate all permutations of remaining (n-1) cities\n"
    "3. For each permutation, compute the tour cost\n"
    "4. Return the permutation with minimum cost\n\n"
    "Time Complexity:  O(n!)     — catastrophically slow\n"
    "Space Complexity: O(n)",
    code_style))
story.append(Spacer(1, 0.3*cm))

growth_data = [
    ["n (cities)", "Permutations (n-1)!", "Approx. time @ 10^9 ops/sec"],
    ["5", "24", "< 1 microsecond"],
    ["10", "362,880", "< 1 millisecond"],
    ["15", "87,178,291,200", "~87 seconds"],
    ["20", "121,645,100,408,832,000", "~3.8 million years"],
    ["25", "≈ 6.2 × 10^23", "Longer than the universe's age"],
]
gt = Table(growth_data, colWidths=[3*cm, 6*cm, 7.5*cm])
gt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8b0000')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Courier'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fff5f5'), colors.white]),
    ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#ffe0e0')),
    ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#ffcccc')),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#c08080')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e0c0c0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
]))
story.append(gt)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph(
    "Key insight: Even doubling your CPU speed only adds ~1 extra city before hitting the same wall. "
    "The factorial growth completely dominates any hardware improvement. This is the fundamental reason "
    "TSP cannot be solved exactly for large inputs by brute force.",
    warning_style))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("4.2 NP-Hardness — What Does It Mean?", h2_style))
story.append(Paragraph(
    "TSP (decision version: 'Is there a tour of cost &lt;= k?') is <b>NP-complete</b>. "
    "The optimisation version (find the minimum tour) is <b>NP-hard</b>. This means:",
    body_style))
story.append(Paragraph("- No polynomial-time algorithm is known that solves all instances optimally", bullet_style))
story.append(Paragraph("- It is believed (but not proven) that no such algorithm exists", bullet_style))
story.append(Paragraph("- TSP is at least as hard as every other problem in NP", bullet_style))
story.append(Paragraph("- This does NOT mean individual instances can't be solved fast — it means the worst case is exponential", bullet_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("4.3 Better Exact Algorithms", h2_style))
complexity_data = [
    ["Algorithm", "Time Complexity", "Feasible up to ~n"],
    ["Brute Force", "O(n!)", "~12 cities"],
    ["Held-Karp DP (Bitmask)", "O(n^2 * 2^n)", "~25 cities"],
    ["Branch & Bound", "Exponential (best case much better)", "~40-50 cities (depends)"],
    ["Approximations (e.g. Christofides)", "O(n^3) — within 1.5x optimal", "Millions of cities"],
]
ct = Table(complexity_data, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (-1,-1), 'Courier'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(ct)
story.append(Spacer(1, 0.4*cm))

story.append(PageBreak())

# ── SECTION 5: BITMASK DP ──────────────────────────────────────────────────────
story.append(Paragraph("5. Held-Karp: Bitmask DP for TSP", h1_style))
story.append(hr())
story.append(Paragraph(
    "The Held-Karp algorithm (1962) is the classic dynamic programming solution for small-to-medium TSP. "
    "It uses a bitmask to represent which cities have been visited.",
    body_style))

story.append(Paragraph("5.1 State Definition", h2_style))
story.append(section_box(
    "dp[mask][i]  =  minimum cost to reach city i, having visited exactly the\n"
    "               cities indicated by the bits in 'mask' (bit j is set if city j visited)\n\n"
    "mask: an integer from 0 to 2^n - 1  (n bits, one per city)\n"
    "i:    the current city (last city visited)\n\n"
    "Base case:   dp[1][0] = 0        (start at city 0, only city 0 visited)\n"
    "Answer:      min over all i of { dp[(1<<n)-1][i] + dist[i][0] }"
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("5.2 Recurrence", h2_style))
story.append(Paragraph(
    "To fill dp[mask][i], consider all possible previous cities j "
    "(j is in mask and j != i):",
    body_style))
story.append(section_box(
    "dp[mask][i]  =  min over all valid j  {  dp[mask without bit i][j]  +  dist[j][i]  }"
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("5.3 Complexity Analysis", h2_style))
story.append(Paragraph("- States: 2^n masks × n cities = n × 2^n states", bullet_style))
story.append(Paragraph("- Transitions: For each state, we check up to n previous cities", bullet_style))
story.append(Paragraph("- Total time: O(n^2 × 2^n)   — much better than O(n!)", bullet_style))
story.append(Paragraph("- Space: O(n × 2^n)", bullet_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "For n = 20: n! ≈ 2.4 × 10^18 vs n^2 × 2^n ≈ 4 × 10^8 operations. "
    "The DP is ~10 billion times faster for n = 20!",
    note_style))

story.append(Spacer(1, 0.5*cm))

# ── SECTION 6: K SHORTEST PATHS ────────────────────────────────────────────────
story.append(Paragraph("6. K Shortest Paths", h1_style))
story.append(hr())
story.append(Paragraph(
    "The <b>k shortest paths problem</b> asks: given source s and destination t, "
    "find the k paths with the lowest total cost (paths may repeat vertices).",
    body_style))

story.append(Paragraph("6.1 Why Not Just Run Dijkstra k Times?", h2_style))
story.append(Paragraph(
    "Dijkstra finds the single shortest path. Running it once gives you the 1st shortest path. "
    "But to get the 2nd, 3rd, ... kth, you cannot simply remove the first path — the paths "
    "are interleaved in complex ways. You need a dedicated algorithm.",
    body_style))

story.append(Paragraph("6.2 Yen's Algorithm (k Shortest Simple Paths)", h2_style))
story.append(Paragraph(
    "Yen's algorithm finds k shortest <i>simple</i> paths (no repeated vertices). Idea:",
    body_style))
story.append(Paragraph("1. Find the 1st shortest path using Dijkstra", bullet_style))
story.append(Paragraph("2. For the p-th path, generate 'spur' paths by iteratively removing edges", bullet_style))
story.append(Paragraph("3. Store candidate paths in a priority queue", bullet_style))
story.append(Paragraph("4. Pop the minimum candidate as the next kth shortest path", bullet_style))
story.append(Paragraph("Time complexity: O(k × n × (m + n log n)) where m = edges", bullet_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("6.3 Priority Queue (Heap) Approach", h2_style))
story.append(Paragraph(
    "A simpler approach (allowing repeated vertices): use a modified Dijkstra with a count array — "
    "the t-th time city v is popped from the priority queue is its t-th shortest distance.",
    body_style))
story.append(Paragraph(
    "dp[v][k]  =  kth shortest distance to vertex v\n"
    "Time complexity: O(k × m × log(n × k))",
    code_style))

story.append(Spacer(1, 0.5*cm))

# ── SECTION 7: REAL-WORLD APPLICATIONS ─────────────────────────────────────────
story.append(Paragraph("7. Real-World Applications", h1_style))
story.append(hr())

apps = [
    ["Domain", "TSP Application"],
    ["Logistics & Delivery", "UPS, FedEx route optimisation (saving millions in fuel per year)"],
    ["Manufacturing", "Drilling order for holes in printed circuit boards"],
    ["DNA Sequencing", "Reconstructing genome sequences from fragments"],
    ["Astronomy", "Optimal telescope pointing order for observations"],
    ["Tourism", "Planning road trips through multiple cities"],
    ["Warehouse Robotics", "Amazon warehouse picking robots"],
]
at = Table(apps, colWidths=[5*cm, 11.5*cm])
at.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(at)
story.append(Spacer(1, 0.5*cm))

# ── SECTION 8: SUMMARY ─────────────────────────────────────────────────────────
story.append(Paragraph("8. Summary & Key Takeaways", h1_style))
story.append(hr())

takeaways = [
    "A Hamiltonian cycle visits every vertex exactly once and returns to start.",
    "TSP = find the minimum-cost Hamiltonian cycle in a weighted complete graph.",
    "Brute force TSP is O(n!) — completely infeasible beyond ~12 cities.",
    "Held-Karp (bitmask DP) reduces this to O(n^2 × 2^n) — feasible up to ~25 cities.",
    "TSP is NP-hard: no polynomial-time exact algorithm is known.",
    "For large instances, approximation algorithms (like Christofides) are used in practice.",
    "K shortest paths extends Dijkstra to find multiple shortest paths efficiently.",
    "Real-world TSP instances with millions of cities are solved using heuristics and specialised solvers.",
]
for i, t in enumerate(takeaways):
    story.append(Paragraph(f"{i+1}.  {t}", bullet_style))
story.append(Spacer(1, 0.4*cm))

story.append(section_box(
    "What to practise next:\n"
    "- Implement Hamiltonian cycle detection using DFS + backtracking\n"
    "- Code brute force TSP and benchmark it for n = 8, 10, 12\n"
    "- Implement Held-Karp bitmask DP for TSP\n"
    "- Try: Codeforces 8C (Looking for Order), SPOJ TSP problems, LeetCode 847",
    bg=colors.HexColor('#e8f0fe')
))

doc.build(story)
print("PDF created successfully.")
