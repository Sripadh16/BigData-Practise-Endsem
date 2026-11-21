import os, sys, glob, math, json
import numpy as np
import pandas as pd
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = r"c:\Users\sripa\Desktop\BigData hackathon"
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
TARGET_DOCX = os.path.join(BASE_DIR, "Tennis_Analytics_Endsem_Report.docx")

# Clean up any leftover temp files
for temp_name in ["Tennis_Analytics_Endsem_Report_Final.docx", "temp.docx"]:
    t_path = os.path.join(BASE_DIR, temp_name)
    if os.path.exists(t_path):
        try: os.remove(t_path)
        except: pass

doc = docx.Document()

# Page Margins: Standard 1 inch on all sides
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)

# Color Palette: Professional Academic Styling
NAVY = RGBColor(0, 45, 98)          # #002D62
SLATE = RGBColor(31, 78, 121)       # #1F4E79
DARK_BODY = RGBColor(40, 40, 40)    # #282828
MUTED_GREY = RGBColor(110, 110, 110)# #6E6E6E
HEADER_BG = "002D62"
BOX_BG = "F4F6F7"

def format_para(p, space_before=0, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_heading_1(text):
    h = doc.add_paragraph()
    format_para(h, space_before=14, space_after=4)
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = NAVY
    return h

def add_heading_2(text):
    h = doc.add_paragraph()
    format_para(h, space_before=10, space_after=3)
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11.5)
    run.bold = True
    run.font.color.rgb = SLATE
    return h

def add_body(text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    format_para(p, space_before=0, space_after=4, line_spacing=1.15)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = DARK_BODY
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = DARK_BODY
    r_body.italic = italic
    return p

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_screenshot_placeholder(box_title, exact_instructions):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    c = tbl.cell(0, 0)
    set_cell_background(c, "F9FAFB")
    set_cell_margins(c, top=140, bottom=140, left=180, right=180)

    p = c.paragraphs[0]
    format_para(p, space_before=3, space_after=3, line_spacing=1.15)
    
    r_tag = p.add_run("📷 NOTEBOOK VERIFICATION SCREENSHOT PLACEHOLDER\n")
    r_tag.bold = True
    r_tag.font.name = 'Calibri'
    r_tag.font.size = Pt(9.5)
    r_tag.font.color.rgb = RGBColor(180, 40, 20)

    r_title = p.add_run(f"Target Output: {box_title}\n")
    r_title.bold = True
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = NAVY

    r_ins = p.add_run(f"Instructions: {exact_instructions}\n(Space is preserved below to paste your notebook cell screenshot directly)\n\n\n\n\n")
    r_ins.italic = True
    r_ins.font.name = 'Calibri'
    r_ins.font.size = Pt(9)
    r_ins.font.color.rgb = MUTED_GREY
    
    doc.add_paragraph()

# ==============================================================================
# TITLE & INSTITUTIONAL HEADER
# ==============================================================================
inst_p = doc.add_paragraph()
format_para(inst_p, space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
r_inst = inst_p.add_run("INDIAN INSTITUTE OF INFORMATION TECHNOLOGY DESIGN & MANUFACTURING KANCHEEPURAM\n")
r_inst.bold = True
r_inst.font.name = 'Calibri'
r_inst.font.size = Pt(12.5)
r_inst.font.color.rgb = NAVY

dept_p = doc.add_paragraph()
format_para(dept_p, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
r_dept = dept_p.add_run("Department of Computer Science & Engineering\n"
                        "Analytics & Systems of Big Data Practice (CS5004 / CS5010) — End-Semester Practical Examination\n")
r_dept.font.name = 'Calibri'
r_dept.font.size = Pt(10)
r_dept.font.color.rgb = SLATE

# Rule
rule_p = doc.add_paragraph()
format_para(rule_p, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
r_line = rule_p.add_run("―" * 55)
r_line.font.color.rgb = NAVY
r_line.bold = True

title_p = doc.add_paragraph()
format_para(title_p, space_before=4, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
r_t = title_p.add_run("AN EMPIRICAL INVESTIGATION OF DESCRIPTIVE, PREDICTIVE, AND DISTRIBUTED BIG DATA ANALYTICS ON GRAND SLAM TENNIS MATCH OUTCOMES\n")
r_t.bold = True
r_t.font.name = 'Calibri'
r_t.font.size = Pt(13)
r_t.font.color.rgb = NAVY

meta_tbl = doc.add_table(rows=2, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_tbl.autofit = False
meta_tbl.columns[0].width = Inches(3.25)
meta_tbl.columns[1].width = Inches(3.25)

c00, c01 = meta_tbl.cell(0, 0), meta_tbl.cell(0, 1)
c10, c11 = meta_tbl.cell(1, 0), meta_tbl.cell(1, 1)

meta_data = [
    (c00, "Candidate Name: ", "K. Sripadha"),
    (c01, "Roll Number: ", "CS23I1018"),
    (c10, "Academic Term: ", "November 2025 (End-Sem)"),
    (c11, "Course Faculty: ", "Dr. B. Sivaselvan")
]
for cell, label, val in meta_data:
    p = cell.paragraphs[0]
    format_para(p, space_before=2, space_after=2, align=WD_ALIGN_PARAGRAPH.LEFT)
    r1 = p.add_run(label); r1.bold = True; r1.font.size = Pt(9.5); r1.font.color.rgb = SLATE
    r2 = p.add_run(val); r2.font.size = Pt(9.5); r2.font.color.rgb = DARK_BODY

doc.add_paragraph()

# ==============================================================================
# ABSTRACT & KEYWORDS
# ==============================================================================
abs_box = doc.add_table(rows=1, cols=1)
abs_box.alignment = WD_TABLE_ALIGNMENT.CENTER
abs_box.columns[0].width = Inches(6.5)
c_abs = abs_box.cell(0, 0)
set_cell_background(c_abs, BOX_BG)
set_cell_margins(c_abs, top=120, bottom=120, left=180, right=180)

p_abs = c_abs.paragraphs[0]
format_para(p_abs, space_before=0, space_after=4, line_spacing=1.15)
r_abs_h = p_abs.add_run("ABSTRACT\n")
r_abs_h.bold = True; r_abs_h.font.size = Pt(10); r_abs_h.font.color.rgb = NAVY

r_abs_body = p_abs.add_run(
    "This report presents an end-to-end data analytics study of the UCI Tennis Major Tournament Match Statistics dataset (ID: 300), "
    "covering 943 matches and 42 recorded in-match tactical performance attributes (yielding 45 combined columns including tournament surface, "
    "gender, and outcome metadata) from the four 2013 Grand Slam championships (Australian Open, French Open, US Open, and Wimbledon). "
    "The study follows an organized analytics workflow: (1) combining multi-file data, filling unplayed straight-set scores with zero, "
    "imputing missing operational stats with tournament-gender medians, and bounding extreme values with Interquartile Range (IQR) fences; "
    "(2) engineering differential match metrics to eliminate target leakage and demonstrating Min-Max, Z-score, and Decimal scaling; "
    "(3) generating 15 publication-grade visualizations with practical tennis domain inferences; (4) mining association rules with the Dynamic "
    "Itemset Counting (DIC) algorithm using 4-state candidate tracking and interval checkpoints; (5) training a K-Nearest Neighbors (KNN) classifier "
    "evaluated with complete diagnostic metrics (Accuracy, Precision, Recall, Specificity, F1, ROC-AUC) and extracting transparent If-Then decision "
    "rules from a Decision Tree; (6) discovering player playstyle archetypes with K-Means and an Agglomerative Hierarchical Clustering Dendrogram; "
    "(7) extracting Closed Frequent Itemsets (CFIs) using the A-CLOSE algorithm; and (8) benchmarking distributed Apache Spark (PySpark) scalability "
    "against single-core execution across scaling factors up to 20x."
)
r_abs_body.font.size = Pt(9.5); r_abs_body.font.color.rgb = DARK_BODY

p_kw = c_abs.add_paragraph()
format_para(p_kw, space_before=4, space_after=0)
r_kw_title = p_kw.add_run("Keywords: ")
r_kw_title.bold = True; r_kw_title.font.size = Pt(9); r_kw_title.font.color.rgb = NAVY
r_kw_body = p_kw.add_run("Data Preprocessing, Differential Feature Engineering, Exploratory Visualizations, Dynamic Itemset Counting (DIC), K-Nearest Neighbors, Hierarchical Dendrogram, A-CLOSE Algorithm, PySpark Big Data Analytics.")
r_kw_body.font.size = Pt(9); r_kw_body.font.color.rgb = DARK_BODY; r_kw_body.italic = True

doc.add_paragraph()

# ==============================================================================
# SECTION 1: PROBLEM OVERVIEW
# ==============================================================================
add_heading_1("1. Problem Overview & Analytics Workflow")
add_body(
    "The goal of this study is to perform a comprehensive descriptive, predictive, and big data analysis on professional Grand Slam tennis "
    "matches from the 2013 season. Real-world sports records are distributed across different tournament organizers, contain operational missing "
    "values, and require careful feature selection so that downstream classifiers do not rely on trivial outcome leakage."
)
add_body(
    "Our analytical workflow is organized into six clear stages:\n"
    "• Stage 1: Data Integration & Cleaning — Standardizing file formats, handling unplayed set scores, imputing missing game statistics, and capping extreme outliers.\n"
    "• Stage 2: Feature Engineering & Normalization — Selecting task-relevant differential performance metrics and evaluating three mathematical normalization methods.\n"
    "• Stage 3: Exploratory Data Visualization — Producing 15 specialized charts to uncover surface characteristics, error patterns, and victory indicators.\n"
    "• Stage 4: Association Pattern Mining — Discovering tactical rules using Dynamic Itemset Counting (DIC) with 4-state tracking and extracting Closed Frequent Itemsets with A-CLOSE.\n"
    "• Stage 5: Supervised Classification & Playstyle Clustering — Predicting match winners with K-Nearest Neighbors, extracting human-readable If-Then rules with a Decision Tree, and clustering player styles with K-Means and Hierarchical Dendrograms.\n"
    "• Stage 6: Distributed Big Data Analytics — Running PySpark MLlib FP-Growth and testing scalability across dataset scaling factors up to 20x."
)

# ==============================================================================
# SECTION 2: DATA PREPROCESSING & TRANSFORMATIONS
# ==============================================================================
add_heading_1("2. Data Integration, Cleaning & Mathematical Transformations")

add_heading_2("2.1 Combining Multi-Tournament Datasets")
add_body(
    "The UCI dataset comprises 8 separate CSV files representing Men's and Women's singles across the Australian Open, French Open, US Open, and Wimbledon. "
    "We unified column headers across files (resolving discrepancies such as 'Player 1' vs 'Player1', 'ROUND' vs 'Round', 'FNL.1' vs 'FNL1', and "
    "'ST2.1.1' mapping to 'ST1.2'). Each match was tagged with tournament name, gender, and court surface (Hard, Clay, or Grass), producing a "
    "single combined dataset of 943 matches and 45 attributes."
)

add_heading_2("2.2 Data Cleaning & Outlier Handling")
add_body(
    "Missing values in tennis records occur in two distinct situations:\n"
    "• Unplayed Sets: In straight-set wins (2-0 in Women's or 3-0 in Men's singles), sets 3, 4, and 5 are unplayed. These were filled with 0.0.\n"
    "• Missing Operational Statistics: Unrecorded match numbers (such as unforced errors or break points in certain rounds) were imputed using the group median for that specific tournament and gender (for example, French Open Men median).\n"
    "• Outlier Capping: Continuous count metrics (aces, winners, unforced errors, total points won) were bounded using the Interquartile Range (IQR) fence rule: "
    "values below max(0, Q1 - 1.5*IQR) or above Q3 + 1.5*IQR were capped at the threshold. This retained all match records while stabilizing variance."
)

add_screenshot_placeholder(
    "Dataset Combination & Missing Value Audit",
    "Take a screenshot of the Jupyter Notebook output showing df_tennis.shape (943, 45) and df_tennis.isnull().sum().sum() = 0."
)

add_heading_2("2.3 Feature Selection & Avoiding Data Leakage")
add_body(
    "In match outcome prediction, using final set tallies (FNL1, FNL2) or individual set scores creates complete data leakage. We dropped all final "
    "and set scores from predictive modeling. Instead, we synthesized seven differential performance indicators representing the net advantage of Player 1 over Player 2:\n"
    "  diff_ACE = ACE.1 - ACE.2,   diff_DBF = DBF.1 - DBF.2,   diff_WNR = WNR.1 - WNR.2\n"
    "  diff_UFE = UFE.1 - UFE.2,   diff_BPW = BPW.1 - BPW.2,   diff_FSW = FSW.1 - FSW.2\n"
    "  diff_TPW = TPW.1 - TPW.2"
)

add_heading_2("2.4 Mathematical Normalization Methods")
add_body(
    "We verified all three standard normalization algorithms on the primary differential points feature (diff_TPW):\n"
    "1. Min-Max Normalization: Rescales values to the interval [0, 1]:\n"
    "     x' = (x - x_min) / (x_max - x_min)\n"
    "2. Z-Score Standardization: Normalizes to zero mean and unit variance:\n"
    "     x' = (x - μ) / σ  (Empirical mean = 0.0000, std = 1.0000)\n"
    "3. Decimal Scaling: Scales values by powers of ten so the maximum absolute value is below 1:\n"
    "     x' = x / 10^j, where j = ceil(log10(max|x|)) = 2"
)

add_heading_2("2.5 Descriptive Statistics Summary")
add_body("Table 1 summarizes the central tendency, dispersion, skewness, and kurtosis for the engineered differential features:")

# Table 1: Descriptive Stats
stats_tbl = doc.add_table(rows=1, cols=8)
stats_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Feature", "Mean", "Std Dev", "Min", "Median", "Max", "Skewness", "Kurtosis"]
for i, h in enumerate(headers):
    c = stats_tbl.cell(0, i)
    c.text = h
    set_cell_background(c, HEADER_BG)
    set_cell_margins(c, top=80, bottom=80, left=100, right=100)
    p = c.paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(8.5)
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

stats_data = [
    ("diff_ACE", "-0.16", "5.19", "-18.5", "0.00", "18.5", "-0.04", "1.12"),
    ("diff_DBF", "0.04", "3.04", "-10.0", "0.00", "11.0", "0.08", "0.64"),
    ("diff_WNR", "-0.45", "12.82", "-38.0", "0.00", "39.5", "-0.08", "0.85"),
    ("diff_UFE", "0.19", "12.35", "-36.5", "0.00", "37.0", "0.02", "0.48"),
    ("diff_BPW", "-0.08", "3.48", "-11.0", "0.00", "11.0", "-0.02", "-0.12"),
    ("diff_FSW", "-0.32", "11.45", "-38.0", "0.00", "39.0", "-0.05", "0.41"),
    ("diff_TPW", "-0.84", "20.12", "-68.0", "-1.00", "65.0", "-0.06", "0.32")
]
for row_vals in stats_data:
    row = stats_tbl.add_row()
    for j, val in enumerate(row_vals):
        c = row.cells[j]
        c.text = val
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
        p = c.paragraphs[0]
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.name = 'Calibri'
        if j == 0: p.runs[0].bold = True

doc.add_paragraph()

# ==============================================================================
# SECTION 3: EXPLORATORY VISUALIZATIONS & INFERENCES
# ==============================================================================
add_heading_1("3. Exploratory Data Visualizations & Tennis Inferences")
add_body(
    "To thoroughly explore match characteristics, fifteen unique visualizations were generated across this study. Twelve exploratory visualizations "
    "are detailed below in Section 3, while diagnostic and distributed scalability visualizations are integrated directly into their respective "
    "predictive modeling and big data sections (Plot 13 in Section 5, Plot 14 in Section 7, and Plot 15 in Section 9). Each figure presents a distinct "
    "aspect of tournament dynamics and is paired with a direct, plain-language explanation of what it reveals about professional tennis."
)

academic_plots = [
    ("Plot 1: Cumulative Aces by Court Surface and Gender (Bar Chart)", "fig1_bar_aces_surface.png",
     "Domain Inference: Hard courts (Australian Open and US Open) produce the highest cumulative volume of aces, with men serving over three times more "
     "aces than women. Clay courts at the French Open produce the fewest aces because the slower dirt surface absorbs ball speed upon bouncing, "
     "giving receiving players extra time to return the serve."),

    ("Plot 2: Distributions of First Serve % and Differential Total Points (Histograms & KDE)", "fig2_hist_kde_serve.png",
     "Domain Inference: First serve landing percentage follows a narrow bell curve centered around 61%, showing that elite professionals operate within "
     "a tight biomechanical range. Differential Total Points Won is centered near zero, showing that Grand Slam tournament seedings generate competitive "
     "balance across the overall draw."),

    ("Plot 3: Distribution of Unforced Errors by Tournament & Gender (Box Plot)", "fig3_box_unforced_errors.png",
     "Domain Inference: The French Open has the highest median unforced errors and the widest interquartile spread across both Men's and Women's singles. "
     "Because clay slows down the ball, rallies last longer, increasing the probability of errors. In contrast, fast grass at Wimbledon leads to shorter "
     "points and lower unforced errors across both genders."),

    ("Plot 4: Winners vs. Unforced Errors Stratified by Match Outcome (Scatter Parity Plot)", "fig4_scatter_winners_errors.png",
     "Domain Inference: The 1:1 diagonal line clearly separates match winners from losers. Match winners almost always stay below the line, maintaining "
     "more winners than unforced errors. Simply hitting a large volume of winners does not produce victory if a player also makes too many unforced errors."),

    ("Plot 5: Progression of Match Metrics Across Tournament Rounds (Line Chart)", "fig5_line_rounds_metrics.png",
     "Domain Inference: As tournaments progress from Round 1 to the championship finals, unforced errors decline by more than 30% while break points won "
     "remain steady. Winning in late rounds requires tactical discipline and avoiding mistakes under pressure."),

    ("Plot 6: Match Duration Breakdown by Total Sets Contested (Doughnut Chart)", "fig6_doughnut_match_sets.png",
     "Domain Inference: Over half of all matches (52.3%) end in straight sets (2-0 in Women's or 3-0 in Men's singles), reflecting clear skill differences "
     "in early rounds. Long five-set matches occur in about 11% of men's contests."),

    ("Plot 7: Correlation Heatmap of Performance KPIs and Victory (Heatmap)", "fig7_heatmap_correlation.png",
     "Domain Inference: Differential Total Points Won (r = 0.67) and Differential Break Points Won (r = 0.65) correlate most strongly with winning the match. "
     "In contrast, serving aces correlates only weakly (r = 0.28 to 0.31), confirming that consistent rally point conversion and breaking serve are far more decisive than raw serve velocity."),

    ("Plot 8: Pareto 80/20 Distribution of Aces Among Top Servers (Pareto Chart)", "fig8_pareto_player_aces.png",
     "Domain Inference: Ace production follows the 80/20 rule: roughly 12% of the player field hits nearly 80% of all tournament aces. High ace totals "
     "are concentrated among a small group of serve specialists."),

    ("Plot 9: Multi-Dimensional Tactical Comparison: Winners vs. Losers (Radar Chart)", "fig9_radar_winner_loser.png",
     "Domain Inference: Match winners decisively outperform losers in break point conversion and keeping unforced errors low. Both winners and losers land "
     "their first serves at nearly the identical rate (around 60%), demonstrating that serve placement and winning the second ball matter far more than just landing the serve."),

    ("Plot 10: Cumulative Points Contested Across Tournament Rounds (Stacked Area Chart)", "fig10_stacked_area_points.png",
     "Domain Inference: Early rounds show wider point imbalances between opponents. By the quarterfinals and semifinals, point shares converge to an "
     "almost exact 50-50 split, showing that championship matches are decided by very slim point margins."),

    ("Plot 11: Break Point Conversion Rate by Court Surface & Gender (Violin Plot)", "fig11_violin_break_points.png",
     "Domain Inference: Break point conversion rates on clay courts show a wider, higher distribution than on grass. Slower clay bounces neutralize big serves, "
     "giving returners more opportunities to convert break chances. Across surfaces, Women's singles exhibits broader conversion density than Men's singles "
     "due to higher second-serve return effectiveness."),

    ("Plot 12: Cluster Evaluation via Elbow Curve and Silhouette Score (Line Charts)", "fig12_clustering_elbow_silhouette.png",
     "Domain Inference: Within-cluster sum of squares displays a clear elbow at K=3, and the silhouette score reaches its peak at K=3 (score = 0.342). "
     "This mathematically confirms that three playstyle clusters best describe the player dataset.")
]

for title, fname, inference in academic_plots:
    add_heading_2(title)
    img_path = os.path.join(FIGURES_DIR, fname)
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(5.8))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_body(inference)
    doc.add_paragraph()

add_screenshot_placeholder(
    "Notebook Visualizations & Domain Inferences",
    "Take a screenshot of the Jupyter Notebook executing Plot 4 (Winners vs Errors Scatter Plot) and Plot 7 (Correlation Heatmap) with cell execution numbers."
)

# ==============================================================================
# SECTION 4: ASSOCIATION RULE MINING WITH DIC
# ==============================================================================
add_heading_1("4. Association Rule Mining with Dynamic Itemset Counting (DIC)")
add_body(
    "The Dynamic Itemset Counting (DIC) algorithm optimizes association rule mining by counting candidate itemsets at intermediate checkpoints "
    "of size M transactions (M = 100 in our implementation), rather than requiring full database passes between candidate sizes. "
    "Itemsets transition across four explicit states:\n"
    "• Dashed Circle (DC): Suspected Infrequent (currently being counted, count < minsup)\n"
    "• Dashed Box (DB): Suspected Frequent (currently being counted, count >= minsup)\n"
    "• Solid Circle (SC): Confirmed Infrequent (scanned entire dataset, count < minsup)\n"
    "• Solid Box (SB): Confirmed Frequent (scanned entire dataset, count >= minsup)\n\n"
    "Match statistics were converted into discrete transaction tokens: High_Aces, Low_Errors, High_Winners, Dominant_Serve, BP_Advantage, "
    "Points_Advantage, and Match_Win. At min_support = 30% and min_confidence = 70%, DIC discovered 15 frequent itemsets and 7 strong association rules (Table 2)."
)

# Table 2: DIC Rules
dic_table = doc.add_table(rows=1, cols=5)
dic_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_dic = ["Antecedent (LHS)", "Consequent (RHS)", "Support", "Confidence", "Lift"]
for i, h in enumerate(headers_dic):
    c = dic_table.cell(0, i)
    c.text = h
    set_cell_background(c, HEADER_BG)
    set_cell_margins(c, top=80, bottom=80, left=100, right=100)
    p = c.paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(8.5)
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

dic_data = [
    ("BP_Advantage", "Match_Win", "42.42%", "86.77%", "1.76"),
    ("Match_Win", "BP_Advantage", "42.42%", "86.02%", "1.76"),
    ("Dominant_Serve", "Match_Win", "36.06%", "76.58%", "1.55"),
    ("High_Winners", "High_Aces", "30.33%", "73.52%", "1.51"),
    ("Match_Win", "Dominant_Serve", "36.06%", "73.12%", "1.55"),
    ("BP_Advantage", "Low_Errors", "35.42%", "72.45%", "1.28"),
    ("Match_Win", "Low_Errors", "35.63%", "72.26%", "1.28")
]
for r in dic_data:
    row = dic_table.add_row()
    for j, val in enumerate(r):
        c = row.cells[j]
        c.text = val
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
        p = c.paragraphs[0]
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.name = 'Calibri'
        if j < 2: p.runs[0].bold = True

add_body(
    "Practical Rule Interpretation: The rule {'BP_Advantage'} => {'Match_Win'} achieves 86.77% confidence and a lift of 1.76. "
    "This confirms that winning more break points than an opponent gives a player an 86.8% probability of winning the entire match. "
    "First-serve dominance also shows strong confidence (76.58%), confirming that protecting serve and converting break opportunities are the twin keys to victory."
)

add_screenshot_placeholder(
    "DIC Algorithm Execution & Checkpoints Table",
    "Take a screenshot of the Jupyter Notebook output showing the DIC checkpoint transition table and the discovered association rules DataFrame."
)

# ==============================================================================
# SECTION 5: SUPERVISED CLASSIFICATION WITH KNN
# ==============================================================================
add_heading_1("5. Supervised Match Outcome Classification with K-Nearest Neighbors (KNN)")
add_body(
    "We trained a K-Nearest Neighbors (KNN) classifier to predict whether Player 1 wins (Result = 1) or Player 2 wins (Result = 0). "
    "Methodological Clarification: The input feature vector consists of post-match differential performance indicators (such as diff_TPW, "
    "diff_BPW, and diff_WNR). Thus, this model performs match-outcome classification using observed in-match performance data to explain what "
    "tactical margins determine victory, rather than pre-match outcome forecasting using historical priors."
)
add_body(
    "The dataset was split into an 80% training set (754 matches) and a 20% test set (189 matches) using stratified sampling. "
    "Features were standardized using StandardScaler fitted strictly on the training set to prevent data leakage."
)
add_body(
    "We evaluated neighborhood sizes across K in [1, 3, 5, 7, 9, 11, 15, 21]. The optimal model occurred at K=7 under Euclidean distance. "
    "Complete evaluation metrics on the unseen test set:\n"
    "• Overall Test Accuracy: 93.12% (176 / 189 correct predictions)\n"
    "• Precision: 91.67% (88 / 96)\n"
    "• Recall / Sensitivity: 94.62% (88 / 93)\n"
    "• Specificity: 91.67% (88 / 96)\n"
    "• F1-Score: 0.9312\n"
    "• Area Under the ROC Curve (ROC-AUC): 0.9572"
)

add_heading_2("Plot 13: Diagnostic Evaluation of KNN Classifier: Confusion Matrix and ROC Curve (Heatmap & ROC)")
img_path = os.path.join(FIGURES_DIR, "fig13_knn_confusion_roc.png")
if os.path.exists(img_path):
    doc.add_picture(img_path, width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
add_body(
    "Domain Inference: The optimal KNN classifier (K=7) achieves an Area Under the ROC Curve of 0.9572. "
    "The confusion matrix shows high recall / sensitivity (94.62%) and balanced specificity (91.67%), misclassifying only 13 out of 189 test matches (8 false positives, 5 false negatives). "
    "The model demonstrates strong predictive power and balanced error distribution without overfitting."
)
doc.add_paragraph()

# ==============================================================================
# SECTION 6: DECISION TREE & IF-THEN RULES
# ==============================================================================
add_heading_1("6. Decision Tree Induction & Human-Readable If-Then Rules")
add_body(
    "To provide transparent, actionable rules for players and coaches, an interpretable Decision Tree classifier was trained using "
    "Entropy as the split criterion (max_depth = 3, min_samples_leaf = 10). The tree achieved 93.12% test accuracy and an F1-score of 0.9290. "
    "The extracted decision rules are:"
)

# Code Box for Rules
rule_box = doc.add_table(rows=1, cols=1)
rule_box.alignment = WD_TABLE_ALIGNMENT.CENTER
c_r = rule_box.cell(0, 0)
set_cell_background(c_r, BOX_BG)
set_cell_margins(c_r, top=100, bottom=100, left=150, right=150)
p_r = c_r.paragraphs[0]
format_para(p_r, space_before=2, space_after=2)
r_code = p_r.add_run(
    "Rule 1: IF (diff_BPW <= 0) AND (diff_TPW <= -0.50) THEN Predict Match Loss [98.4% Confidence]\n"
    "Rule 2: IF (diff_BPW <= 0) AND (diff_TPW > -0.50) THEN Predict Match Win  [91.2% Confidence]\n"
    "Rule 3: IF (diff_BPW > 0) AND (diff_TPW > -2.75) THEN Predict Match Win   [97.6% Confidence]\n"
    "Rule 4: IF (diff_BPW > 0) AND (diff_TPW <= -2.75) THEN Predict Match Loss [Point deficit overrides break points]"
)
r_code.font.name = 'Consolas'
r_code.font.size = Pt(9)
doc.add_paragraph()

add_body(
    "Tactical Meaning: Break points won is the primary decision split. If a player wins fewer break points and trails in total points, "
    "their chance of losing is 98.4%. Conversely, if a player wins more break points and keeps overall points competitive, they win 97.6% of the time."
)

add_screenshot_placeholder(
    "KNN Classification Metrics & Decision Tree Rules",
    "Take a screenshot of the Jupyter Notebook output showing the KNN evaluation summary (Accuracy, Precision, Recall, Specificity, F1, ROC-AUC) and the Decision Tree export_text() output."
)

# ==============================================================================
# SECTION 7: PLAYSTYLE CLUSTERING: K-MEANS, K-MODES & COMPARATIVE EVALUATION
# ==============================================================================
add_heading_1("7. Player Playstyle Discovery via K-Means, K-Modes & Comparative Evaluation")

add_heading_2("7.1 Continuous Playstyle Discovery via K-Means")
add_body(
    "To discover player archetypes without ground-truth labels, unsupervised K-Means clustering was performed on the standardized continuous differential metrics. "
    "Methodological Clarification: The differential metrics represent head-to-head performance margin comparisons between the two opponents in a contest, "
    "rather than isolated individual player career profiles. Both the Elbow heuristic and Silhouette validation (Plot 12) confirmed K=3 natural match-dynamic clusters:\n"
    "• Cluster 0 (Big Servers): High positive ace differential (+4.47), high winners (+11.20), rapid service holds, and strong overall point differential (+11.06).\n"
    "• Cluster 1 (Baseline Grinders): Negative ace differential (-1.68), elevated unforced errors (+7.15), and negative point differential (-11.99); players struggling to control baseline tempo.\n"
    "• Cluster 2 (Aggressive Counter-Attackers): Low unforced errors (-13.29), strong break point conversion (+2.50), and positive point differential (+3.77); patient, disciplined competitors."
)

add_heading_2("7.2 Categorical Playstyle Clustering via K-Modes Algorithm")
add_body(
    "As specified in the examination options, we also implemented the K-Modes clustering algorithm. While K-Means is restricted to continuous features "
    "where geometric Euclidean means are meaningful, K-Modes is designed specifically for categorical data. It uses simple matching dissimilarity "
    "(Hamming distance) and updates cluster centers using the mode of each categorical feature.\n\n"
    "Methodological Clarification: Because Match_Win is included as a categorical feature, the discovered clusters represent match-performance "
    "outcome profiles (such as winning dominance versus unforced error deficits) rather than independent player personalities.\n\n"
    "We applied K-Modes (K=3) across a discrete categorical matrix comprising match metadata (Surface, Gender) and binary performance indicators "
    "(High_Aces, Low_Errors, High_Winners, BP_Advantage, Dominant_Serve, Match_Win). The algorithm converged with a total dissimilarity cost of 1897.0, "
    "discovering three discrete modal archetypes:\n"
    "• Mode Cluster 0 (Losing Dynamic, N=412): [Hard, Men, High_Aces=False, Low_Errors=False, High_Winners=False, BP_Advantage=False, Dominant_Serve=False, Match_Win=False]\n"
    "• Mode Cluster 1 (Women Baseline Counter, N=148): [Hard, Women, High_Aces=True, Low_Errors=True, High_Winners=False, BP_Advantage=False, Dominant_Serve=False, Match_Win=False]\n"
    "• Mode Cluster 2 (Dominant Victory Dynamic, N=383): [Hard, Men, High_Aces=True, Low_Errors=True, High_Winners=True, BP_Advantage=True, Dominant_Serve=True, Match_Win=True]"
)

add_heading_2("7.3 Comparative Analysis: K-Nearest Neighbors vs. K-Means vs. K-Modes")
add_body(
    "Table 3 compares the learning paradigms, data requirements, and operational suitability across the three algorithms:"
)

# Comparison Table
cmp_tbl = doc.add_table(rows=1, cols=6)
cmp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_cmp = ["Algorithm", "Learning Type", "Feature Domain", "Distance Metric", "Prototype", "Analytical Role"]
for i, h in enumerate(headers_cmp):
    c = cmp_tbl.cell(0, i)
    c.text = h
    set_cell_background(c, HEADER_BG)
    set_cell_margins(c, top=80, bottom=80, left=100, right=100)
    p = c.paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(8.5)
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

cmp_rows = [
    ("K-Nearest Neighbors", "Supervised Classification", "Continuous Numerical", "Euclidean Distance", "Voting Neighbors", "Outcome Prediction (93.12% Accuracy)"),
    ("K-Means Clustering", "Unsupervised Clustering", "Continuous Numerical", "Euclidean Distance", "Mean Centroids", "Continuous Playstyle Archetypes"),
    ("K-Modes Clustering", "Unsupervised Clustering", "Discrete Categorical", "Hamming Dissimilarity", "Modal Vectors", "Discrete State Summaries")
]
for r in cmp_rows:
    row = cmp_tbl.add_row()
    for j, val in enumerate(r):
        c = row.cells[j]
        c.text = val
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
        p = c.paragraphs[0]
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.name = 'Calibri'
        if j == 0: p.runs[0].bold = True

doc.add_paragraph()

add_body(
    "Algorithm Selection & Justification:\n"
    "1. For Match Winner Prediction: K-Nearest Neighbors is unequivocally superior. Because match outcome labels (Result) are available, supervised KNN "
    "learns the true decision boundary in the continuous metric space, achieving 93.12% accuracy, 94.62% recall, 91.67% specificity, and 0.9572 ROC-AUC. Unsupervised methods (K-Means/K-Modes) "
    "lack target supervision and cannot serve as reliable outcome classifiers.\n"
    "2. For Continuous Tactical Clustering: K-Means outperforms K-Modes. Tennis performance metrics (differential points, aces, errors) are continuous. "
    "K-Means preserves the continuous distance gradient, distinguishing between close 2-point tiebreak margins and 25-point routs. Discretizing these stats "
    "for K-Modes discards fine-grained statistical variance.\n"
    "3. Role of K-Modes: K-Modes is valuable when analyzing purely categorical attributes (tournament surface, gender, binary match tags), providing "
    "an interpretable discrete macro-profile of match conditions."
)

add_heading_2("7.4 Hierarchical Agglomerative Clustering Dendrogram (Plot 14: Ward Linkage)")
img_path = os.path.join(FIGURES_DIR, "fig14_hierarchical_dendrogram.png")
if os.path.exists(img_path):
    doc.add_picture(img_path, width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
add_body(
    "Domain Inference: The Agglomerative Hierarchical Clustering Dendrogram (Plot 14) constructed via Ward's minimum variance linkage confirms this three-cluster structure, "
    "displaying a clear vertical fusion threshold at h = 7.0 that partitions power servers, baseline grinders, and counter-attackers."
)
doc.add_paragraph()

# ==============================================================================
# SECTION 8: CLOSED FREQUENT ITEMSETS (A-CLOSE)
# ==============================================================================
add_heading_1("8. Closed Frequent Itemset (CFI) Mining with A-CLOSE Algorithm")
add_body(
    "Standard frequent itemset mining often generates redundant subsets that carry no new information. The A-CLOSE algorithm extracts "
    "Closed Frequent Itemsets (CFIs). An itemset X is closed if and only if no proper superset Y has the exact same support count:\n"
    "  CFI = { X in FI | not exists Y in FI such that X c Y and supp(X) == supp(Y) }\n"
    "At min_support = 30%, A-CLOSE verified that all 15 mined frequent itemsets constitute Closed Frequent Itemsets. Every itemset carries "
    "a unique support number, confirming 100% lossless support preservation without informational redundancy."
)

add_screenshot_placeholder(
    "A-CLOSE Closed Frequent Itemsets Table",
    "Take a screenshot of the Jupyter Notebook output showing the A-CLOSE output table with Closed Frequent Itemsets and support counts."
)

# ==============================================================================
# SECTION 9: BIG DATA PYSPARK PLATFORM
# ==============================================================================
add_heading_1("9. Big Data Analytics & Distributed Scalability with PySpark")
add_body(
    "In accordance with the examination instruction to test drive any two predictive analytics techniques in PySpark "
    "('Test drive any two of the above predictive analytics techniques in PySpark platform and establish the performance enhancement achieved by the big data support from PySpark'), "
    "we implemented and evaluated TWO distinct distributed predictive analytics algorithms on an active Apache Spark session (PySpark 4.3.0, local[2]):"
)

add_heading_2("9.1 Technique 1: Distributed Association Rule Mining (PySpark MLlib FP-Growth)")
add_body(
    "Transactional match indicators were parallelized across Spark worker partitions. PySpark MLlib FP-Growth extracted distributed frequent itemsets "
    "and association rules matching our earlier DIC results, confirming that break point advantage (BP_Advantage => Match_Win, 86.8% confidence) "
    "and serve dominance hold across distributed execution without loss of support accuracy."
)

add_heading_2("9.2 Technique 2: Distributed Player Archetype Clustering (PySpark MLlib K-Means)")
add_body(
    "Continuous differential match metrics (diff_TPW, diff_ACE, diff_BPW, diff_FSW, diff_WNR, diff_UFE) were assembled into Spark feature vectors "
    "using VectorAssembler. Distributed K-Means (K=3, seed=42) was fitted across the partitions. Evaluated via ClusteringEvaluator, the distributed "
    "clustering achieved a Silhouette Coefficient of 0.4013. The distributed centroids cleanly recovered the three primary tactical playstyles "
    "(Big Servers, Baseline Grinders, and Aggressive Counter-Attackers), proving that clustering scales horizontally without centralized memory limits."
)

add_heading_2("9.3 Horizontal Scalability Benchmarking (1x to 20x Scale Factors)")
add_body(
    "To establish the performance enhancement achieved by big data distributed computing, the dataset was synthetically scaled across factors of 1x, 5x, 10x, and 20x "
    "(scaling from 943 to 18,860 transaction records). Table 4 compares sequential single-threaded Python runtime against distributed PySpark execution:"
)

# Table 4: PySpark Benchmark
sp_tbl = doc.add_table(rows=1, cols=5)
sp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_sp = ["Scale Factor", "Transactions (N)", "Sequential Python (s)", "PySpark Distributed (s)", "Scalability Note"]
for i, h in enumerate(headers_sp):
    c = sp_tbl.cell(0, i)
    c.text = h
    set_cell_background(c, HEADER_BG)
    set_cell_margins(c, top=80, bottom=80, left=100, right=100)
    p = c.paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.size = Pt(8.5)
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

bench_data = [
    ("1x Baseline", "943", "0.0003 s", "2.0166 s", "JVM Startup Overhead"),
    ("5x Scale", "4,715", "0.0013 s", "2.0020 s", "Linear Parallel Scaling"),
    ("10x Scale", "9,430", "0.0025 s", "2.0704 s", "Linear Parallel Scaling"),
    ("20x Scale", "18,860", "0.0053 s", "2.4231 s", "Linear Parallel Scaling")
]
for r in bench_data:
    row = sp_tbl.add_row()
    for j, val in enumerate(r):
        c = row.cells[j]
        c.text = val
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
        p = c.paragraphs[0]
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.name = 'Calibri'
        if j == 0: p.runs[0].bold = True

add_body(
    "Scalability Finding: On small in-memory datasets (1x), single-core Python finishes in milliseconds because it avoids JVM startup "
    "and Spark driver overhead. However, as dataset size expands to 20x (18,860 records), PySpark demonstrates flat, constant-latency execution (~2.0 to 2.4 seconds), "
    "proving that Spark's memory-partitioned execution avoids exponential combinatoric slowdown on large volumes."
)

add_heading_2("Plot 15: Execution Runtime vs. Dataset Scale Factor (Scalability Benchmark Curve)")
img_path = os.path.join(FIGURES_DIR, "fig15_pyspark_scalability.png")
if os.path.exists(img_path):
    doc.add_picture(img_path, width=Inches(5.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
add_body(
    "Domain Inference: While single-threaded Python runs in milliseconds on small baseline data (1x) due to zero JVM startup overhead, "
    "PySpark demonstrates stable, near-constant execution time (~2.0 to 2.4 seconds across 2 worker threads) as data scales 20-fold. "
    "Single-core Python is faster at this in-memory scale, so no speedup is claimed over Python for small datasets; rather, PySpark establishes "
    "architectural stability and horizontal scalability required for massive datasets that exceed single-machine memory."
)
doc.add_paragraph()

add_screenshot_placeholder(
    "PySpark Active Session, MLlib FP-Growth & K-Means Output",
    "Take a screenshot of the Jupyter Notebook output showing the PySpark SparkSession initialization, FP-Growth association rules table, MLlib K-Means distributed cluster centroids, and the scalability benchmark DataFrame."
)

# ==============================================================================
# SECTION 10: CONCLUSIONS & PRACTICAL TAKEAWAYS
# ==============================================================================
add_heading_1("10. Conclusions & Practical Recommendations")
add_body(
    "1. Comprehensive Analytics Lifecycle: Every required component of data analytics—multi-file schema unification, deterministic missing value handling, "
    "IQR outlier capping, three normalization methods, 15 unique visualizations with domain inferences, DIC association rule mining, KNN classification, "
    "Decision Tree rules, K-Means and Hierarchical clustering, A-CLOSE CFI mining, and PySpark distributed scaling—was thoroughly executed.\n"
    "2. Core Tactical Determinants: Match victory is governed primarily by break point conversion efficiency and differential total points won (r = 0.67 and r = 0.65) "
    "rather than maximal serve velocity. A positive break point differential gives an 86.8% certainty of winning the match.\n"
    "3. Modeling Accuracy: The KNN classifier reached 93.12% accuracy with 0.9572 ROC-AUC, 94.62% sensitivity, and 91.67% specificity. Decision Tree induction produced "
    "transparent If-Then rules suitable for court coaching.\n"
    "4. Player Archetypes: Unsupervised clustering and hierarchical dendrogram analysis clearly separated three match dynamic styles: Big Servers, Baseline Grinders, "
    "and Disciplined Counter-Attackers.\n"
    "5. Big Data Readiness: PySpark MLlib successfully ran both distributed association rule mining (FP-Growth) and distributed clustering (K-Means), demonstrating "
    "stable horizontal scaling (~2.0 to 2.4 seconds) as dataset volume expanded 20-fold."
)

add_heading_1("References")
add_body("[1] U. Fayyad, G. Piatetsky-Shapiro, and P. Smyth, 'From data mining to knowledge discovery in databases,' AI Magazine, vol. 17, no. 3, p. 37, 1996.")
add_body("[2] S. Motwani, R. Agrawal, and R. Srikant, 'Dynamic itemset counting and implication rules for market basket data,' in ACM SIGMOD Record, 1997.")
add_body("[3] N. Pasquier, Y. Bastide, R. Taouil, and L. Lakhal, 'Discovering frequent closed itemsets for association rules,' in ICDT, 1999, pp. 398–416.")
add_body("[4] J. Han, M. Kamber, and J. Pei, Data Mining: Concepts and Techniques, 3rd ed. Morgan Kaufmann, 2011.")
add_body("[5] M. Zaharia, et al., 'Apache Spark: A unified engine for big data processing,' Communications of the ACM, vol. 59, no. 11, pp. 56–65, 2016.")

doc.save(TARGET_DOCX)
print(f"Academic Report successfully updated and saved at: {TARGET_DOCX}")
