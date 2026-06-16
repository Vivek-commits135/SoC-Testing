from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# =========================================================================
# CONFIGURATION
# =========================================================================
OUTPUT_PDF_NAME = "Theory.pdf"
# =========================================================================

doc = SimpleDocTemplate(
    OUTPUT_PDF_NAME,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
    fontSize=26, textColor=colors.HexColor('#1a1a2e'), spaceAfter=6,
    fontName='Helvetica-Bold', alignment=TA_CENTER)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontSize=13, textColor=colors.HexColor('#4a4a8a'), spaceAfter=20,
    alignment=TA_CENTER, fontName='Helvetica-Oblique')
h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
    fontSize=18, textColor=colors.HexColor('#1a1a2e'),
    spaceBefore=18, spaceAfter=6, fontName='Helvetica-Bold')
h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=14, textColor=colors.HexColor('#2d4070'),
    spaceBefore=12, spaceAfter=4, fontName='Helvetica-Bold')
body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=11, textColor=colors.HexColor('#222222'), spaceAfter=8,
    leading=17, alignment=TA_JUSTIFY, fontName='Helvetica')
note_style = ParagraphStyle('Note', parent=styles['Normal'],
    fontSize=10.5, textColor=colors.HexColor('#1a3a1a'),
    backColor=colors.HexColor('#e8f5e8'), fontName='Helvetica-Oblique',
    leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6,
    leading=15, borderPad=8)
warning_style = ParagraphStyle('Warning', parent=styles['Normal'],
    fontSize=10.5, textColor=colors.HexColor('#3a1a00'),
    backColor=colors.HexColor('#fff3e0'), fontName='Helvetica',
    leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6,
    leading=15, borderPad=8)
bullet_style = ParagraphStyle('BulletItem', parent=styles['Normal'],
    fontSize=11, textColor=colors.HexColor('#222222'),
    leftIndent=20, spaceAfter=4, leading=16, bulletIndent=8)

def hr():
    return HRFlowable(width="100%", thickness=1.2,
                      color=colors.HexColor('#c0c8e0'), spaceAfter=8, spaceBefore=4)

def section_box(text, bg=colors.HexColor('#eef0fb')):
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
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#b0b8d8')),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (0,0), 8),
        ('BOTTOMPADDING', (-1,-1), (-1,-1), 8),
        ('TOPPADDING', (0,1), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-2), 1),
    ]))
    return t

def make_table(data, col_widths, header_bg='#2d4070'):
    cell_style = ParagraphStyle('cell', parent=styles['Normal'], fontSize=10, leading=13)
    cell_bold = ParagraphStyle('cellB', parent=styles['Normal'], fontSize=10, leading=13, fontName='Helvetica-Bold')
    header_style = ParagraphStyle('header', parent=styles['Normal'], fontSize=10, leading=13, textColor=colors.white, fontName='Helvetica-Bold')

    formatted_data = []
    for i, row in enumerate(data):
        formatted_row = []
        for j, text in enumerate(row):
            text_str = str(text).replace('<', '&lt;').replace('>', '&gt;')
            if i == 0:
                p = Paragraph(text_str, header_style)
            elif j == 0:
                p = Paragraph(text_str, cell_bold)
            else:
                p = Paragraph(text_str, cell_style)
            formatted_row.append(p)
        formatted_data.append(formatted_row)

    t = Table(formatted_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(header_bg)),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t

story = []

# ── COVER ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("Week 4: TSP Introduction", title_style))

story.append(Spacer(1, 0.4*cm))

# Meta Table Removed as requested

# ── SECTION 1: GRAPH RECAP ─────────────────────────────────────────────────────
story.append(Paragraph("1. Quick Graph Recap", h1_style))
story.append(hr())
story.append(Paragraph(
    "Before diving into Hamiltonian cycles and TSP, make sure the following vocabulary is "
    "rock-solid. These ideas will appear constantly in competitive programming.",
    body_style))

story.append(make_table([
    ["Term", "Definition", "Example"],
    ["Vertex (node)", "A point/city in the graph", "City A, City B ..."],
    ["Edge", "A connection between two vertices", "Road from A to B"],
    ["Weight", "Cost/distance assigned to an edge", "Distance = 42 km"],
    ["Degree", "Number of edges touching a vertex", "City A has 3 roads"],
    ["Path", "Sequence of vertices, no repeated vertex", "A -> B -> C -> D"],
    ["Cycle", "A path that starts and ends at the same vertex", "A -> B -> C -> A"],
    ["Complete graph Kn", "Every pair of vertices is connected", "K4 has 6 edges"],
    ["Connected graph", "Path exists between every pair of vertices", "All cities reachable"],
], [4*cm, 7.5*cm, 5*cm]))
story.append(Spacer(1, 0.5*cm))

# ── SECTION 2: EULERIAN CYCLE ──────────────────────────────────────────────────
story.append(Paragraph("2. Eulerian Cycle", h1_style))
story.append(hr())

story.append(Paragraph("2.1 Formal Definition", h2_style))
story.append(Paragraph(
    "An <b>Eulerian cycle</b> (also called an Eulerian circuit) is a cycle in a graph that "
    "<b>traverses every edge exactly once</b> and returns to the starting vertex. "
    "Vertices may be revisited — it is edges that must each appear exactly once.",
    body_style))

story.append(section_box(
    "Definition — Eulerian Cycle:\n"
    "A cycle that uses every edge of the graph exactly once.\n"
    "Vertices can be visited more than once.\n\n"
    "Existence condition (undirected graph):\n"
    "  The graph is connected AND every vertex has even degree.\n\n"
    "Existence condition (directed graph):\n"
    "  The graph is strongly connected AND\n"
    "  in-degree(v) = out-degree(v) for every vertex v."
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("2.2 The Famous Origin — Konigsberg Bridge Problem", h2_style))
story.append(Paragraph(
    "In 1736, Leonhard Euler solved the Konigsberg Bridge Problem: can you walk through the city "
    "crossing each of its 7 bridges exactly once and return to your starting point? Euler proved "
    "it was impossible because the graph had vertices with odd degree. This was the birth of "
    "graph theory itself. The key insight: an Eulerian cycle exists if and only if every vertex "
    "has even degree (in an undirected connected graph).",
    body_style))

story.append(Paragraph("2.3 Finding an Eulerian Cycle — Hierholzer's Algorithm", h2_style))
story.append(Paragraph(
    "Once you know an Eulerian cycle exists, finding it is efficient:",
    body_style))
story.append(section_box(
    "Hierholzer's Algorithm:\n"
    "1. Start at any vertex, follow edges (removing them) until you return to start.\n"
    "   This gives a partial cycle C.\n"
    "2. If C uses all edges: done.\n"
    "3. Otherwise, find a vertex in C that still has unused edges.\n"
    "4. Start a new sub-cycle from that vertex, splice it into C.\n"
    "5. Repeat until all edges are used.\n\n"
    "Time Complexity: O(E)  — incredibly fast, linear in number of edges!"
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "The O(E) complexity of Eulerian cycle detection and construction stands in stark contrast "
    "to the exponential complexity of Hamiltonian cycle problems — this difference is one of "
    "the most striking examples of how similar-sounding problems can have wildly different complexities.",
    note_style))
story.append(Spacer(1, 0.4*cm))

# ── SECTION 3: HAMILTONIAN CYCLE ───────────────────────────────────────────────
story.append(Paragraph("3. Hamiltonian Cycle", h1_style))
story.append(hr())

story.append(Paragraph("3.1 Formal Definition", h2_style))
story.append(Paragraph(
    "A <b>Hamiltonian cycle</b> (also called a Hamiltonian circuit) is a cycle that "
    "<b>visits every vertex exactly once</b> and returns to the starting vertex. "
    "Unlike Eulerian cycles, it is edges that may be skipped — every vertex must appear exactly once.",
    body_style))

story.append(section_box(
    "Definition — Hamiltonian Cycle:\n"
    "Given a graph G with n vertices, a Hamiltonian cycle is a sequence\n"
    "  v0, v1, v2, ..., v(n-1), v0\n"
    "such that:\n"
    "  (1)  Each vi is a distinct vertex of G\n"
    "  (2)  Each consecutive pair (vi, v(i+1)) is an edge in E\n"
    "  (3)  The pair (v(n-1), v0) is also an edge in E  (closing the cycle)\n\n"
    "There is NO simple polynomial-time test for existence (it is NP-complete)."
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("3.2 Sufficient Conditions (Not Necessary)", h2_style))
story.append(Paragraph("- <b>Dirac (1952):</b> If every vertex has degree &gt;= n/2, a Hamiltonian cycle exists.", bullet_style))
story.append(Paragraph("- <b>Ore (1960):</b> If deg(u) + deg(v) &gt;= n for every non-adjacent pair, a Ham. cycle exists.", bullet_style))
story.append(Paragraph("- <b>Complete graphs Kn (n &gt;= 3):</b> Always have a Hamiltonian cycle.", bullet_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("3.3 Hamiltonian Path vs. Hamiltonian Cycle", h2_style))
story.append(make_table([
    ["Property", "Hamiltonian Path", "Hamiltonian Cycle"],
    ["Visits all vertices?", "Yes", "Yes"],
    ["Returns to start?", "No", "Yes"],
    ["Edges used", "n - 1", "n"],
    ["Application", "Route planning (one-way)", "TSP, circular routes"],
], [4.5*cm, 6*cm, 6*cm]))
story.append(Spacer(1, 0.5*cm))

# ── SECTION 4: EULERIAN vs HAMILTONIAN ─────────────────────────────────────────
story.append(Paragraph("4. Eulerian vs. Hamiltonian — The Critical Difference", h1_style))
story.append(hr())
story.append(Paragraph(
    "These two cycle types are often confused by beginners. They sound similar but are fundamentally "
    "different in what they require and how hard they are to solve.",
    body_style))

story.append(make_table([
    ["Property", "Eulerian Cycle", "Hamiltonian Cycle"],
    ["What must appear exactly once?", "Every EDGE", "Every VERTEX"],
    ["Can edges be skipped?", "No", "Yes"],
    ["Can vertices be revisited?", "Yes", "No"],
    ["Existence: easy to check?", "YES — O(V+E) via degree check", "NO — NP-complete"],
    ["Finding one (if exists)?", "YES — O(E) Hierholzer", "NO — exponential (brute force)"],
    ["Key constraint", "Even degree at all vertices", "No simple polynomial condition"],
    ["Complexity class", "P (polynomial time)", "NP-complete"],
], [4.5*cm, 6*cm, 6*cm]))
story.append(Spacer(1, 0.4*cm))


story.append(Paragraph("4.1 A Concrete Example", h2_style))
story.append(Paragraph(
    "Consider a square graph: vertices A, B, C, D connected in a cycle A-B-C-D-A "
    "with one diagonal B-D added.",
    body_style))
story.append(Paragraph("- Eulerian cycle: Does one exist? Degrees: A=2, B=3, C=2, D=3. Vertex B and D have odd degree. "
    "NO Eulerian cycle.", bullet_style))
story.append(Paragraph("- Hamiltonian cycle: A -> B -> C -> D -> A visits all 4 vertices exactly once. "
    "YES, Hamiltonian cycle exists.", bullet_style))
story.append(Paragraph("- Same graph, opposite answers — this illustrates they are independent properties!", bullet_style))
story.append(Spacer(1, 0.5*cm))

story.append(PageBreak())

# ── SECTION 5: TSP ─────────────────────────────────────────────────────────────
story.append(Paragraph("5. The Travelling Salesman Problem (TSP)", h1_style))
story.append(hr())

story.append(Paragraph("5.1 Problem Statement", h2_style))
story.append(section_box(
    "TSP — Formal Statement:\n"
    "Given a complete weighted graph G = (V, E, w) where w(u,v) is the cost of edge (u,v),\n"
    "find a Hamiltonian cycle of minimum total weight.\n\n"
    "Input:  n cities, pairwise distances d[i][j]\n"
    "Output: A permutation of cities (a tour) that visits each city exactly once\n"
    "        and returns to start, minimising the total travel cost."
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("5.2 Variants of TSP", h2_style))
story.append(make_table([
    ["Variant", "Key Constraint", "Notes"],
    ["Symmetric TSP", "d[i][j] = d[j][i]", "Most common; undirected graph"],
    ["Asymmetric TSP", "d[i][j] may not equal d[j][i]", "Directed graph (one-way roads)"],
    ["Metric TSP", "Triangle inequality holds", "Allows approximation guarantees"],
    ["Euclidean TSP", "Cities are points in 2-D plane", "Special case of metric TSP"],
], [4*cm, 6*cm, 6.5*cm]))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("5.3 Worked Example (n = 4)", h2_style))
story.append(Paragraph("Cities: 0 (Home), 1, 2, 3. Distance matrix:", body_style))

dist_data = [
    ["", "0", "1", "2", "3"],
    ["0", "0", "10", "15", "20"],
    ["1", "10", "0", "35", "25"],
    ["2", "15", "35", "0", "30"],
    ["3", "20", "25", "30", "0"],
]
ddt = Table(dist_data, colWidths=[2.5*cm]*5)
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

tour_b = ParagraphStyle('tourB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)
tour_n = ParagraphStyle('tourN', parent=styles['Normal'], fontName='Courier', fontSize=10)
tour_opt = ParagraphStyle('tourOpt', parent=styles['Normal'], fontName='Courier-Bold', fontSize=10)

tours_data = [
    [Paragraph("Tour", tour_b), Paragraph("Cost Calculation", tour_b), Paragraph("Total", tour_b)],
    [Paragraph("0-&gt;1-&gt;2-&gt;3-&gt;0", tour_n), Paragraph("10 + 35 + 30 + 20", tour_n), Paragraph("95", tour_n)],
    [Paragraph("0-&gt;1-&gt;3-&gt;2-&gt;0", tour_n), Paragraph("10 + 25 + 30 + 15", tour_n), Paragraph("80  &lt;- OPTIMAL", tour_opt)],
    [Paragraph("0-&gt;2-&gt;1-&gt;3-&gt;0", tour_n), Paragraph("15 + 35 + 25 + 20", tour_n), Paragraph("95", tour_n)],
]
tours_table = Table(tours_data, colWidths=[4.5*cm, 8*cm, 4*cm])
tours_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d4070')),
    ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#d4edda')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f6fc'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#b0b8d8')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#dde0f0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(tours_table)
story.append(Spacer(1, 0.5*cm))

# ── SECTION 6: COMPLEXITY ──────────────────────────────────────────────────────
story.append(Paragraph("6. Why is TSP Hard? NP-Hardness", h1_style))
story.append(hr())

story.append(Paragraph("6.1 Brute Force", h2_style))
story.append(section_box(
    "Fix city 0 as start. Try all (n-1)! permutations of the remaining cities.\n\n"
    "Time Complexity:  O(n!)   -- catastrophically slow\n"
    "Space Complexity: O(n)"
))
story.append(Spacer(1, 0.3*cm))

story.append(make_table([
    ["n (cities)", "Permutations checked", "Approx. time @ 10^9 ops/sec"],
    ["5", "24", "< 1 microsecond"],
    ["10", "362,880", "< 1 millisecond"],
    ["15", "87,178,291,200", "~87 seconds"],
    ["20", "121,645,100,408,832,000", "~3.8 million years"],
    ["25", "~6.2 x 10^23", "Longer than the universe's age"],
], [4*cm, 7*cm, 5.5*cm], header_bg='#8b0000'))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "Key insight: Even doubling your CPU speed only lets you handle ~1 extra city before "
    "hitting the same wall. Factorial growth completely dominates any hardware improvement.",
    warning_style))
story.append(Spacer(1, 0.4*cm))

# ── SECTION 6.2 (REPLACEMENT) ──────────────────────────────────────────────────
story.append(Paragraph("6.2 NP-Hardness and NP-Completeness", h2_style))

story.append(Paragraph(
    "To accurately describe the complexity of TSP, we must distinguish between its two forms: "
    "the <b>Decision Version</b> and the <b>Optimization Version</b>. The way we classify "
    "their difficulty relies on understanding P, NP, NP-Complete, and NP-Hard.",
    body_style))

# Using the section_box function defined earlier in your script
story.append(section_box(
    "Complexity Classes Refresher:\n"
    "• P: Problems that can be SOLVED in polynomial time.\n"
    "• NP: Problems where a proposed solution can be VERIFIED in polynomial time.\n"
    "• NP-Hard: Problems that are 'at least as hard as the hardest problems in NP'.\n"
    "• NP-Complete: Problems that are BOTH in NP and are NP-Hard."
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>The Decision Version (NP-Complete)</b>", body_style))
story.append(Paragraph(
    "<i>Question: 'Given a graph and a budget K, does there exist a tour with a total cost &lt;= K?'</i>",
    body_style))
story.append(Paragraph(
    "This version is <b>NP-Complete</b>. First, it belongs to NP: if someone hands you a sequence of cities, "
    "you can easily add up the edge weights in O(n) time and verify if the sum is indeed &lt;= K. Second, it is "
    "NP-Hard because any other problem in NP can be mathematically translated (reduced) into this problem in polynomial time.",
    body_style))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>The Optimization Version (NP-Hard)</b>", body_style))
story.append(Paragraph(
    "<i>Question: 'What is the absolute minimum cost Hamiltonian cycle in the graph?'</i>",
    body_style))
story.append(Paragraph(
    "This version is <b>NP-Hard</b>, but technically NOT in NP. Why? Because if someone hands you a tour and "
    "claims 'This is the absolute shortest possible route', there is no quick (polynomial time) way to verify that claim. "
    "To prove it is the optimal tour, you would theoretically have to compare it against other tours. "
    "It is 'at least as hard' as the decision version, but it lacks the quick verification property of NP.",
    body_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Conclusions:</b>", body_style))
story.append(Paragraph("- <b>No known fast exact algorithm:</b> Nobody has found a way to solve all TSP instances optimally in polynomial time (like O(n^2) or O(n^3)).", bullet_style))
story.append(Paragraph("- <b>P vs NP:</b> It is widely believed by computer scientists that P != NP, meaning such a fast, exact algorithm likely does not exist.", bullet_style))
story.append(Paragraph("- <b>Worst-case vs Average-case:</b> 'NP-Hard' describes the absolute worst-case scenario. Many real-world instances have specific structures (like metric or Euclidean properties) that allow solvers to find exact answers quickly despite the theoretical worst-case classification.", bullet_style))
story.append(Spacer(1, 0.5*cm))

# ── SECTION 7: TSP EXACT ALGORITHMS ───────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("7. Some Exact Algorithms (Optional)", h1_style))
story.append(hr())

story.append(Paragraph("7.1 Held-Karp: Bitmask DP", h2_style))
story.append(Paragraph(
    "The Held-Karp algorithm (1962) uses dynamic programming with a bitmask to represent "
    "which cities have been visited. It is the classic exact solution for small-to-medium TSP.",
    body_style))

story.append(Paragraph("State Definition", h2_style))
story.append(section_box(
    "dp[mask][i]  =  minimum cost to reach city i, having visited exactly the\n"
    "               cities indicated by the bits in mask (bit j set = city j visited)\n\n"
    "mask: an integer from 0 to 2^n - 1  (n bits, one per city)\n"
    "i:    the current city (last city visited)\n\n"
    "Base case:   dp[1][0] = 0        (start at city 0, only city 0 visited)\n"
    "Answer:      min over all i of { dp[(1<<n)-1][i] + dist[i][0] }"
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Recurrence", h2_style))
story.append(Paragraph(
    "To fill dp[mask][i], consider all possible previous cities j (j is in mask, j != i):",
    body_style))
story.append(section_box(
    "dp[mask][i]  =  min over all valid j  {  dp[mask ^ (1<<i)][j]  +  dist[j][i]  }"
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Complexity", h2_style))
story.append(Paragraph("- States: 2^n masks x n cities = n x 2^n total states", bullet_style))
story.append(Paragraph("- Transitions: For each state, check up to n previous cities", bullet_style))
story.append(Paragraph("- Total time: O(n^2 x 2^n)   -- much better than O(n!)", bullet_style))
story.append(Paragraph("- Space: O(n x 2^n)", bullet_style))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "For n = 20: n! is about 2.4 x 10^18 vs n^2 x 2^n is about 4 x 10^8 operations. "
    "Held-Karp is roughly 10 billion times faster for n = 20.",
    note_style))
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("7.2 Branch and Bound", h2_style))
story.append(Paragraph(
    "Branch and Bound algorithms explore the search space (like a tree of partial tours) and maintain a 'lower bound' "
    "on the cost of completing a partial tour. If a partial tour's lower bound exceeds the best complete tour "
    "found so far, that branch is entirely pruned. This drastically reduces the search space compared to brute force, "
    "though worst-case time is still exponential.",
    body_style))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("7.3 Integer Linear Programming (ILP) &amp; Branch-and-Cut", h2_style))
story.append(Paragraph(
    "TSP can be formulated mathematically as an ILP problem (using subtour elimination constraints like the "
    "Miller-Tucker-Zemlin formulation). Advanced commercial solvers like Concorde use cutting-plane methods "
    "combined with Branch and Bound (called Branch-and-Cut) to solve massive TSP instances with thousands of cities exactly.",
    body_style))
story.append(Spacer(1, 0.5*cm))

# ── SECTION 8: ADVANCED PARADIGMS TO EXPLORE ──────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("8. Advanced Algorithmic Paradigms to Explore (Optional)", h1_style))
story.append(hr())

story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("8.1 Deep Dive: What is an Approximation Algorithm?", h2_style))
story.append(Paragraph(
    "When a problem is NP-hard, finding the exact optimal solution in polynomial time is considered impossible. "
    "An <b>Approximation Algorithm</b> is a deterministic algorithm that runs in <b>polynomial time</b> and provides "
    "a mathematically provable guarantee on the quality of the solution compared to the true optimal solution.",
    body_style))

story.append(Paragraph(
    "This quality guarantee is expressed as an <b>approximation ratio (ρ)</b>. For a minimization problem like TSP, "
    "if the algorithm produces a tour of cost C and the absolute minimum cost is C*, the algorithm guarantees: "
    "<b>C &lt;= ρ * C*</b>. For example, a '1.5-approximation' means the generated path will never be more than 50% "
    "longer than the best path possible, no matter how chaotic or massive the graph is.",
    body_style))

story.append(Paragraph("8.2 Brief Overview of Approximation Schemes", h2_style))
story.append(Paragraph("<b>2-Approximation via MST:</b> Constructs a Minimum Spanning Tree, runs a DFS traversal, and shortcuts duplicates. It guarantees a tour cost &lt;= 2x optimal in graphs satisfying the triangle inequality.", bullet_style))
story.append(Paragraph("<b>Christofides Algorithm:</b> Combines an MST with a minimum-weight perfect matching on odd-degree nodes to form an Eulerian subgraph. It provides an exceptional 1.5x optimality guarantee in polynomial time.", bullet_style))

story.append(Paragraph("8.3 Brief Overview of Heuristic Paradigms", h2_style))
story.append(Paragraph(
    "Unlike approximation algorithms, <b>Heuristics</b> and <b>Local Search</b> methods don't provide rigorous "
    "provable guarantees. However, they are incredibly fast and produce near-optimal solutions in practice.",
    body_style))

story.append(make_table([
    ["Strategy Type", "Core Heuristic Idea", "Typical Performance"],
    ["Nearest Neighbour", "Greedy method: start anywhere and always jump to the nearest unvisited city.", "Fast O(n^2), yields paths roughly 20-25% above optimal."],
    ["2-opt Local Search", "Iteratively alters a path by swapping pairs of edges to untangle crossings.", "Extremely popular; routinely gets within 5% of optimal."],
    ["Lin-Kernighan (LK)", "An advanced local search that dynamically changes the number of edge swaps per pass.", "The practical gold standard; typically finishes within 1-2% of optimal."],
], [3.5*cm, 7.5*cm, 5.5*cm]))
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph("8.4 Paradigm &amp; Complexity Matrix", h2_style))
story.append(make_table([
    ["Algorithm", "Type Paradigm", "Time Complexity", "Quality Guarantee"],
    ["Brute Force", "Exact (Permutations)", "O(n!)", "Optimal (Exact)"],
    ["Held-Karp DP", "Exact (Bitmask DP)", "O(n^2 * 2^n)", "Optimal (Exact)"],
    ["Branch & Bound", "Exact (Search & Prune)", "Exponential (Varies)", "Optimal (Exact)"],
    ["ILP (Branch-and-Cut)", "Exact (Optimization)", "Exponential (Varies)", "Optimal (Exact)"],
    ["MST 2-Approx", "Approximation", "O(n^2)", "Within 2.0x OPT (Strict bound)"],
    ["Christofides", "Approximation", "O(n^3)", "Within 1.5x OPT (Strict bound)"],
    ["Nearest Neighbour", "Greedy Heuristic", "O(n^2)", "No provable bound (Practical execution)"],
    ["2-opt Search", "Local Search Heuristic", "O(n^2) per pass", "No provable bound (Near-optimal practical)"],
], [3.5*cm, 4.5*cm, 4*cm, 4.5*cm]))
story.append(Spacer(1, 0.5*cm))

# ── SECTION 9: REAL-WORLD APPLICATIONS ────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("9. Real-World Applications", h1_style))
story.append(hr())
story.append(Paragraph(
    "TSP and its variants appear across an enormous range of industries. Understanding the "
    "problem deeply helps you recognise when a real situation is reducible to TSP.",
    body_style))

story.append(Paragraph("9.1 Logistics and Last-Mile Delivery", h2_style))
story.append(Paragraph(
    "This is the most direct application. Companies like UPS, FedEx, DHL, and Amazon Logistics "
    "route tens of thousands of delivery vehicles every day. UPS's ORION system uses a variant "
    "of TSP with time windows (TSPTW) to optimise 55,000 routes daily for 66,000 drivers.",
    body_style))

story.append(Paragraph("9.2 Food Delivery and Hyper-Local Logistics", h2_style))
story.append(Paragraph(
    "Food delivery platforms like Swiggy, Zomato, DoorDash, and UberEats face real-time, highly dynamic variations of the TSP. "
    "Delivery partners must pick up multiple orders from different restaurants and deliver them to various customer locations "
    "while minimizing total travel time and ensuring the food stays hot. This is mathematically modeled as a dynamic "
    "Vehicle Routing Problem with Time Windows (VRPTW).",
    body_style))

story.append(Paragraph("9.3 Printed Circuit Board (PCB) Manufacturing", h2_style))
story.append(Paragraph(
    "When manufacturing a circuit board, a drill must punch thousands of tiny holes. The drill head "
    "must visit each hole exactly once. A board with 10,000 holes requires solving a 10,000-city Euclidean TSP instance.",
    body_style))

story.append(Paragraph("9.4 Genome Sequencing and Bioinformatics", h2_style))
story.append(Paragraph(
    "In DNA sequencing, a genome is broken into millions of short 'read' fragments. "
    "Reassembling these into the original sequence involves finding the shortest superstring "
    "that contains all fragments — this problem is NP-hard and is closely related to TSP.",
    body_style))

story.append(make_table([
    ["Domain", "Specific Problem", "Scale in Practice"],
    ["Package Delivery", "UPS/FedEx daily routing (TSPTW)", "55,000 routes, 10M+ stops/day"],
    ["Food Delivery Apps", "Dynamic VRPTW (Pickups/Drop-offs)", "Millions of orders, real-time recalculation"],
    ["PCB Manufacturing", "Drill head path planning", "1,000 - 100,000 holes per board"],
    ["Genome Assembly", "Shortest superstring / Hamiltonian path", "Millions of reads per genome"],
    ["Telescope Scheduling", "Minimise slewing time between targets", "Hundreds of targets per night"],
    ["Warehouse Robots", "Amazon Kiva multi-shelf item collection", "Millions of items, 1000s of robots"],
], [4*cm, 6.5*cm, 6*cm]))
story.append(Spacer(1, 0.5*cm))

story.append(Paragraph("9.5 The Chinese Postman Problem — Eulerian in Practice", h2_style))
story.append(Paragraph(
    "The Chinese Postman Problem (also called Route Inspection) asks: given a graph representing "
    "streets, find the shortest walk that traverses every edge at least once and returns to start. "
    "Real applications include: street sweeper routing, snow plough routing, and mail carrier routing.",
    body_style))
story.append(Spacer(1, 0.4*cm))


# ── SECTION 10: EXTERNAL RESOURCES & PRACTICE ─────────────────────────────────
story.append(PageBreak()) # Puts resources on a fresh, clean page
story.append(Paragraph("10. External Resources", h1_style))
story.append(hr())


story.append(Paragraph("<b>Theoretical Deep Dives</b>", h2_style))
story.append(Paragraph("• <b>Christofides Algorithm:</b> Essential reading for understanding 1.5x approximation guarantees in metric graphs.", bullet_style))
story.append(Paragraph("• <b>Lin-Kernighan Heuristic (LKH):</b> Research the variable-depth K-opt swaps that power the world's most successful heuristic TSP solvers.", bullet_style))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Industry-Grade Solvers</b>", h2_style))
story.append(Paragraph("• <b>Google OR-Tools:</b> An open-source software suite by Google for optimization. Excellent for Vehicle Routing Problems (VRP) and TSP.", bullet_style))
story.append(Paragraph("• <b>Concorde TSP Solver:</b> The undisputed champion of exact TSP solvers, famous for solving an 85,900-city instance optimally.", bullet_style))
story.append(Spacer(1, 0.3*cm))



# =========================================================================
# BUILD PDF
# =========================================================================
doc.build(story)
print("Updated PDF generated successfully.")
