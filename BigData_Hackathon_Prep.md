# 📚 BigData Hackathon — Study Reference Guide

> [!IMPORTANT]
> 1. **Core Priority (Course Topics First):** The topics, concepts, and algorithms covered in the course syllabus (all the topics documented in this guide) MUST be definitely present and applied first in tomorrow's hackathon analysis and report. Extra/advanced algorithms, methods, or packages can then be added as enhancements if relevant.
> 2. **Big Data / Scalability (Use PySpark):** If the dataset is large, **use PySpark**. Run FP-Growth, K-Means, and any heavy processing through PySpark for the Big Data Analysis section. Compare PySpark performance vs non-parallelized version — this directly fulfils the "Big Data Analysis" requirement in the report.
> **CS5002 Analytics & Systems of Big Data** | Prof. B. Sivaselvan, IIITDM Kancheepuram
> *Save this. Tomorrow, share the question paper and I'll divide the work into phases for you.*

---

## 🗂️ Course Structure at a Glance

The course has **3 pillars** (from Lecture 1):
| Pillar | Description |
|--------|-------------|
| **A. Descriptive Analytics** | What is in the data — stats, plots, distributions |
| **B. Predictive Analytics** | What will happen — classification, clustering |
| **C. Systems / Big Data Storage** | Efficient analytics at scale — PySpark, parallelization |

**Hackathon report must cover all three** with inferences, graphs, screenshots, conclusions.

---

## 📖 Lecture-by-Lecture Summary

### Lectures 1–3: Course Intro, Data Science Overview, Data Analytics

**Core idea (Lec 2):** Data Mining = non-trivial extraction of hidden, previously unknown and potentially useful information from large databases.

**Key distinction:**
- **DBMS** → retrieves explicitly stored info (queries)
- **Data Mining / KDD** → projects info *not explicitly stored* → discovers hidden patterns

**Four analytics types (Lec 1 Alternate View):**
1. **Descriptive** — *what* part of data
2. **Diagnostic** — *why* for the what
3. **Predictive** — what is likely to occur in future
4. **Prescriptive** — suggest future actions to avoid/reach states

**Real-world applications taught:**
- Gmail: spam classification, priority inbox (frequent patterns), subject mining
- Amazon: anticipatory shipping, association rules ("people who bought C++ also bought Java")
- Netflix: pause/rewind/rating → "those who watched House of Cards UK also watched Kevin Spacey films"
- Banking: loan risk classification, fraudulent card analysis (outlier detection)
- Uber, LinkedIn PYMK, Healthcare PharmacoVigilance

**Data Mining Techniques (Lec 2):**
- Data Classification
- Association Rule Mining
- Clustering
- Prediction
- Outlier Mining
- Multimedia Data Mining (Text/Audio/Video)

---

### Lecture 4: Data Representation Mechanisms (Visualization Theory)

**Chart types taught with their pros/cons:**

| Chart | Use Case | Key Formula / Note |
|-------|----------|--------------------|
| **Pie Chart** | Proportions | % = (value/total)×100; Degree = (value/total)×360 |
| **Histogram** | Distribution | "bins" — no gaps between bars; shows skewness |
| **Dot Plot** | Small datasets | Cluttered >20–30 points; use boxplot instead |
| **Stem-Leaf Plot** | Shape + exact values | Impractical for large data |
| **Scatter Plot** | Relationships | +ve/-ve/no correlation; does NOT imply causation |
| **Box Plot** | Five-number summary | Min, Q1, Median, Q3, Max; whiskers = outlier boundary |

**Histogram shapes to recognize:**
- Normal Distribution (bell), Bimodal (two humps), Right Skewed, Left Skewed

**Box Plot interpretation rule:**
- Non-overlapping boxes → groups are different
- Overlapping but medians outside → likely different
- Short box = consistent data; Taller box = more variable

---

### Lecture 5: KDD Phases (Critical for Report Structure)

**KDD Pipeline — always frame your report around this:**
```
Raw Data
  → Cleaning (missing values, noise, outliers, inconsistencies)
  → Integration (combining multiple data sources)
  → Selection (choosing relevant attributes)
  → Transformation (normalization, discretization, encoding)
  → Data Mining (classification, association, clustering, etc.)
  → Pattern Evaluation (interestingness, metrics)
  → Knowledge Presentation (decision trees, rules, visualizations)
```

**Data Quality dimensions:**
- Accuracy, Completeness, Consistency, Timeliness, Believability, Interpretability

**Missing Data handling strategies (taught):**
1. Ignore the tuple
2. Fill manually
3. Global constant (e.g., "unknown")
4. Attribute mean / class-conditional mean
5. Most probable value (Bayesian / decision tree inference)

**Noisy Data — Binning (Lab 4 topic):**
- Sort → partition into equal-frequency bins
- Smooth by: **bin means**, **bin medians**, **bin boundaries**

**Data Reduction strategies:**
- Dimensionality reduction: PCA, Wavelet Transforms, Feature Subset Selection
- Numerosity reduction: Regression, Histograms, Clustering, Sampling
- Data compression

---

### Lecture 6–9: Association Rule Mining (Frequent Itemset Mining)

#### Core Concepts
- **Association Rule:** X → Y (disjoint itemsets)
- **Support:** P(X ∪ Y) — rule significance; fraction of transactions containing both
- **Confidence:** P(Y|X) = support(X∪Y)/support(X) — certainty degree
- **Strong Association Rule:** meets both min_support AND min_confidence
- **Lift:** Confidence / P(Y) — >1 means positive correlation

**Apriori Property (Anti-monotonicity):**
> *"All nonempty subsets of a frequent itemset must also be frequent."*
> If itemset I is infrequent → I∪A is also infrequent (prune supersets)

**Two phases of Association Rule Mining:**
1. Frequent Itemset Generation
2. Strong Association Rule Generation: for each frequent itemset l, output `s ⇒ (l-s)` if confidence ≥ min_conf

#### Algorithms — What Each Does

| Algorithm | Lecture | Key Idea | Improvement Over |
|-----------|---------|----------|-----------------|
| **Apriori** | 6 | Level-wise; generates candidates from Lk, prunes by anti-monotonicity | Baseline |
| **FP-Growth** | 6–7 | Compresses DB into FP-tree; mines conditional pattern bases recursively; only 2 DB scans | Apriori (no repeated scans) |
| **DIC** | 8 | Dynamic Itemset Counting; block-based; 4 states: solid/dashed × box/circle; adds candidates mid-scan | Apriori (fewer scans) |
| **Hash Variant (DHP)** | 9 | Hash pair occurrences into buckets; prune buckets below min_support before counting | Reduces candidate 2-itemsets |
| **Transaction Reduction** | 9 | Tracks SOT (Size Of Transaction); removes transactions too small to hold any Ck | Saves scan time |
| **Vertical (Eclat)** | 9 | Stores TID-sets per item; pair support = |TID(A) ∩ TID(B)| | Avoids repeated DB scans |
| **Partitioning** | 9 | Split DB → local frequent itemsets per partition → global candidates from union | Parallelizable |

#### DIC States (from Lecture 8 trace):
- **Solid box** ✅ → confirmed frequent
- **Solid circle** ❌ → confirmed infrequent
- **Dashed box** ◻ → suspected frequent (still counting)
- **Dashed circle** ◯ → suspected infrequent (still counting)

#### FP-Tree Construction (Lecture 7):
1. Scan DB → find frequent items → sort by frequency descending
2. Reorder each transaction by frequency order
3. Build tree: shared prefixes stored together; each node = (item, count)
4. Mine conditional pattern bases for each item

#### Lab 6 Results (chess.txt: 3,196 tx, 75 items, 37 avg length):
| Support | Confidence | Frequent Itemsets | Rules | Apriori Time | FP-Growth Time |
|---------|------------|------------------|-------|-------------|----------------|
| 20% | 70% | 1,215 | 1,299 | 0.39s | 0.65s |
| 30% | 80% | 946 | 912 | 0.44s | 0.63s |
| 40% | 90% | 713 | 552 | 0.34s | 0.38s |

**Key observation:** Both produce same itemset counts (same problem); Apriori slightly faster on dense data at length-2 limit; FP-Growth scales better generally.

---

### Lecture 10–12: Closed & Maximal Frequent Itemsets (CFI / MFI)

#### Closed Frequent Itemsets (CFI)
> *A frequent itemset is closed if no proper superset has exactly the same support.*

- **Contains complete support information** (can derive support of any subset)
- Mined by **AClose** algorithm
- Two functions: `t(x)` = transactions containing x; `i(y)` = items in every transaction of y
- Closure: `f(x) = i(t(x))` — applied until stable
- **Minimal Generator** = smallest set whose closure is a given closed set

#### Maximal Frequent Itemsets (MFI)
> *A frequent itemset is maximal if none of its immediate supersets is frequent.*

- **More compact** than CFI but loses support info (can't recover exact support of subsets)
- Mined by **Pincer Search**

#### AClose Algorithm (Lecture 11):
1. Find minimal generators (candidates with sufficient support)
2. Discard sets with same support as a subset (not minimal generators)
3. Apply closure `f(x) = i(t(x))` to each generator → get closed sets

#### Pincer Search (Lecture 12):
- **Bottom-up:** Apriori-style frequent itemset search
- **Top-down:** Maintains MFCS (Maximal Frequent Candidate Sets)
- When infrequent candidate found → refine MFCS (remove item from candidates)
- Result: maximal frequent itemsets

#### Lab 8 Results (chess.txt, support=0.95):
| Algorithm | Output Type | Count |
|-----------|------------|-------|
| Partitioning Apriori | All frequent itemsets | 77 |
| AClose | Closed frequent itemsets | 73 |
| Pincer Search | Maximal frequent itemsets | 11 |

---

### Lecture 13: Data Classification

**Classification = Supervised Learning**
- Build model from labeled training data → predict class of unseen data
- 2-step: **Training Phase** (learn model) → **Testing Phase** (apply model)

#### Decision Tree (ID3 / CART / C4.5)
- Greedy, top-down, recursive divide-and-conquer
- Stop when: all samples same class | no attributes left (majority vote) | no samples left

**Splitting Criteria:**
| Criterion | Algorithm | Formula |
|-----------|-----------|---------|
| **Information Gain** | ID3 | $IG(A) = H(\text{parent}) - \sum \frac{|D_j|}{|D|} H(D_j)$ |
| **Entropy** | ID3/C4.5 | $H(D) = -\sum_{j} p_j \log_2 p_j$ |
| **Gain Ratio** | C4.5 | $GR(A) = \frac{Gain(A)}{SplitInfo(A)}$ — corrects bias toward many-valued attrs |
| **Gini Index** | CART | $Gini(D) = 1 - \sum p_j^2$ — minimize for best split |

**Lab 9 key result (Bank Marketing, 41,188 records, 11.3% positive class):**
- Unconstrained tree: 4,931 nodes, 100% train accuracy, **F1=0.5367** (overfitting)
- Depth-5 Entropy: **F1=0.6037, ROC-AUC=0.9408** (61 nodes)
- Depth-3: **F1=0.6105** — optimal balance
- Root split: `nr.employed ≤ 5087.65` (macroeconomic indicator)

**Evaluation Metrics (all taught):**
| Metric | Formula |
|--------|---------|
| Precision | $p = \frac{TP}{TP+FP}$ |
| Recall (Sensitivity) | $r = \frac{TP}{TP+FN}$ |
| Specificity | $\frac{TN}{TN+FP}$ |
| F1-Score | Harmonic mean of p and r |
| AUC-ROC | Area under TPR vs FPR curve; perfect=1, random=0.5 |

---

### Lecture 14: Naive Bayes Classification

**Bayes' Theorem:**
$$P(H|X) = \frac{P(X|H) \cdot P(H)}{P(X)}$$

**Naive assumption:** All attributes are conditionally independent given class → product of individual probabilities.

$$P(C_i|X) \propto P(C_i) \times \prod_{k=1}^{n} P(x_k | C_i)$$

**Gaussian NB** (continuous attributes):
$$P(x_k | C_i) = \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

**Laplacian Correction** (zero-probability problem): Add 1 to each count to avoid zero likelihood.

**Lab 10 datasets used:**
- Supply Chain Logistics (N=100, 24 attrs, multi-class)
- UCI Online Shoppers Intention (N=12,330, 18 attrs, binary)

**Advantages:** Easy, fast, good in practice
**Disadvantages:** Independence assumption → loss of accuracy when features correlated

---

### Lectures 15–17: Genetic Algorithms

**GA Inspiration:** Natural selection — fittest survive and reproduce

**Canonical GA Flow:**
```
Initialize Population → Fitness Evaluation → Selection → Crossover → Mutation → [repeat until STOP]
```

**Key Representations:**
- **Gene:** one bit of binary string
- **Chromosome:** full binary string (encoding one solution)
- **Individual:** a candidate solution (one or more chromosomes)
- **Population:** group of individuals
- **Fitness function:** measure of solution quality (must be positive; higher = better)

**GA Operators:**
| Operator | Description |
|----------|-------------|
| **Roulette Wheel Selection** | Probability ∝ fitness; fitter individuals selected more often |
| **Tournament Selection** | Pick k random, take best |
| **Single-Point Crossover** | Random cut; swap tails between two parents (prob = $p_c$) |
| **Two-Point Crossover** | Two cuts; swap middle segment |
| **Mutation** | Flip each bit with prob $p_m$ (maintains diversity) |

**Schema Theorem (Lecture 16):**
> Short-defining-length, low-order, above-average-fitness schemata receive exponentially increasing instances in successive generations.

$$E[m(H,k+1)] \geq m(H,k) \cdot \frac{f(H,k)}{\bar{f}} \cdot \left(1 - p_c \frac{\delta(H)}{l-1}\right)(1-p_m)^{o(H)}$$

**Lab 12 — GA for 5-variable optimization:**
- Functions: 5D Rastrigin (multimodal, ~11^5 local minima) and 5D Rosenbrock (banana valley)
- Chromosome: 80 bits (16 bits per variable)
- Operators tested: Tournament/Roulette/Rank selection; Single/Two-point/Uniform crossover

**Bucket Brigade Classifier System (Lecture 17):** GA applied to rule-based classifiers; credit apportionment mechanism.

**EVO-Tree pseudocode (from slides):**
```
1. Random initial population of trees
2. Compute fitness of each tree
3. Repeat: Select → Crossover/Mutate → Compute fitness → Update population
4. Until stopping criteria
```

---

### Lectures 18–19: Neural Networks

**Key concepts (from slides):**
- Fully connected, supervised, inductive/classification learning
- Learns by **adjusting weights** to correctly classify training data
- High tolerance to noisy/incomplete data; long training time

**MLFF (Multi-Layer Feed-Forward) Architecture:**
- Input layer: one node per attribute
- Hidden layer(s): arbitrary number; often 1–2
- Output layer: one node per class (multi-class) or 1 node (binary)
- Feed-forward: no cycles back to input or previous layer

**Backpropagation Steps:**
1. Initialize weights (small random values) and biases
2. Feed training sample (forward pass with activation function)
3. Propagate inputs forward
4. Backpropagate error (compare prediction vs actual)
5. Update weights and biases
6. Repeat with terminating condition

**Activation function:** Sigmoid, used at each hidden/output unit.

---

### Lecture 20–22: Clustering

**Clustering = Unsupervised Learning** — grouping without labels

#### K-Means (Lecture 20)
1. Initialize K centroids (furthest apart points or random)
2. Assign each point to nearest centroid (Euclidean distance)
3. Recompute centroid = mean of cluster points
4. Repeat until stable
5. Verify: each point closer to own centroid than others; relocate if not

**Lab 10 step-by-step example (N=7, K=2):**
- After iterations: Cluster1={1,2}, Cluster2={3,4,5,6,7}
- Individual 3 reassigned from Cluster1 (closer to Cluster2 mean)
- **Elbow Method:** plot WCSS vs K; choose elbow point

#### Hierarchical Clustering (Lectures 20–21)
- **Agglomerative (bottom-up):** Each object = own cluster → merge closest pair iteratively
- **Divisive (top-down):** All in one cluster → split recursively

**Linkage methods:**
| Linkage | Distance Formula |
|---------|-----------------|
| **Single** | min{d(x_ip, x_jq)} — nearest neighbor |
| **Complete** | max{d(x_ip, x_jq)} — furthest neighbor |
| **Average** | avg{d(x_ip, x_jq)} |
| **Ward** | Minimizes total within-cluster variance |

**Dendrogram:** Y-axis = distance at which clusters merged (cluster height); cut height determines K.

**Lifetime:** Distance from cluster creation to its next merge.
**K-cluster Lifetime:** Time from K clusters emerging to K-1 clusters (longer = more natural K).

#### DBSCAN (Lab 11)
- **eps** (ε): neighborhood radius
- **min_samples** (MinPts): min points to be core
- Point types:
  - **Core point:** |N_ε(p)| ≥ MinPts
  - **Border point:** reachable from core, but not core itself
  - **Noise:** neither core nor border
- **Advantage:** finds arbitrary shapes, identifies outliers, no need to specify K
- **Disadvantage:** struggles with varying density, high dimensions

---

### Lecture 22: Similarity Measures

**Euclidean Distances:**
| Norm | Formula | Name |
|------|---------|------|
| L₂ | √(Σ(xᵢ-yᵢ)²) | Euclidean (most common) |
| L₁ | Σ|xᵢ-yᵢ| | Manhattan / City-block |
| L∞ | max|xᵢ-yᵢ| | Chebyshev |

**Non-Euclidean Distances:**
| Measure | Formula | Use Case |
|---------|---------|----------|
| **Jaccard** | 1 - |A∩B|/|A∪B| | Sets / binary vectors |
| **Cosine** | arccos(p₁·p₂ / |p₁||p₂|) | Text, high-dimensional |
| **Edit (Levenshtein)** | #inserts + #deletes to transform one string to another | Strings |
| **Hamming** | # positions where bit-vectors differ | Binary strings |

**Axioms of a valid distance measure:** d(x,y)>0; d(x,y)=0 iff x=y; d(x,y)=d(y,x); Triangle inequality d(x,y)≤d(x,z)+d(z,y).

---

## 🔬 Lab Submissions Summary

| Lab | Dataset | Key Methods Used | Key Results/Findings |
|-----|---------|-----------------|---------------------|
| **Lab 1** | Provided sales/order data | Excel: SUM, AVERAGE, MEDIAN, STDEV, COUNTIF, SUMIF, SUMPRODUCT, PERCENTILE, QUARTILE, NETWORKDAYS, DATEDIF; Data Analysis: Descriptive Stats, Correlation, Covariance, Sampling | Statistical summary table; found strong correlations |
| **Lab 2** | Sales data + Tableau (Titanic, Netflix, Volcanoes) | Bar, Histogram, Pie, Scatter, Line charts | Europe = highest sales ($9.6M); 54% consumer segment; Sales peak mid-year |
| **Lab 3** | income2024, Netflix | Doughnut, Pareto, Radar, Area, Heatmap (seaborn, matplotlib, plotly) | COMPLETE orders = 34%; top 15 of 49 categories → 94.4% sales (Pareto 80-20); Netflix: 68.4% movies |
| **Lab 4** | incom2024 (15,549 rows), NPCI AEPS/NACH 2025–2026 | Min-Max, Z-score, Decimal Scaling normalization; Binning (mean/median/boundary); Reduction by grouping | Normalization transformed sales_per_customer to [0,1]; discounts grouped for avg sales analysis |
| **Lab 5** | Smart City Digital Twin (9 CSVs → 538,770 rows, 55 cols) | Integration (district_id+timestamp keys), duplicate removal, IQR outlier clipping, Log1p + sqrt transform, LabelEncoder, One-Hot Encoding, feature engineering (temporal features) | Merged 8 datasets; dropped high-nullity cols (>97%); zero missing values and duplicates after preprocessing |
| **Lab 6** | chess.txt (3,196 tx, 75 items) | Apriori, FP-Growth; support 20–40%, confidence 70–90%; timing comparison across dataset sizes | Same itemsets; Apriori slightly faster on dense data; FP-Growth better generally |
| **Lab 7** | chess.txt | DIC, Hash Apriori, Vertical Transaction | Different representations; all correct on same support; timing varies by method |
| **Lab 8** | chess.txt + synthetic (10 tx, ABCD) | Partitioning Apriori, AClose, Pincer Search | Synthetic: 9 frequent, 9 closed, 5 maximal; Chess (95% sup): 77/73/11 |
| **Lab 9** | Bank Marketing UCI (41,188 rows, 21 cols) | Decision Tree (Gini + Entropy), hyperparameter tuning, confusion matrix, ROC-AUC, tree tracing | Depth-3 entropy: F1=0.6105; AUC=0.9408; root node: nr.employed ≤ 5087.65 |
| **Lab 10** | Supply Chain (N=100), Online Shoppers (N=12,330); Synthetic clustering (N=500) | Gaussian/Bernoulli/Multinomial Naive Bayes; K-Means (elbow), Hierarchical (ward/complete/single/average), dendrogram | NB classification results; K-Means identified 4 clusters on synthetic; dendrograms visualized |
| **Lab 11** | UCI Wine (178), Penguins (333), Breast Cancer (569), Ames Housing, Titanic (889), Online Shoppers (12,330) | DBSCAN (eps, min_samples tuning), 13 numerical similarity metrics, 11 categorical metrics, Gower distance, 11 advanced clustering algos (OPTICS, spectral, affinity propagation, GMM, etc.) | DBSCAN sensitive to eps/scaling; curse of dimensionality at 30D; Gower handles mixed types |
| **Lab 12** | Synthetic (GA benchmarks), Colab/PySpark | GA (5-var Rastrigin + Rosenbrock), TSP with GA, FP-Growth in PySpark, DBSCAN in PySpark, 5 classifiers + clustering | 80-bit chromosome (5×16); Tournament/Roulette/Rank selection tested; PySpark parallels vs sequential comparison |

---

## 📊 Normalization Formulas (Lab 4)

| Method | Formula | Range |
|--------|---------|-------|
| **Min-Max** | $x' = \frac{x - x_{min}}{x_{max} - x_{min}}$ | [0, 1] |
| **Z-Score** | $x' = \frac{x - \mu}{\sigma}$ | (−∞, +∞) |
| **Decimal Scaling** | $x' = \frac{x}{10^j}$, where $j = \lceil \log_{10}(\max|x|) \rceil$ | (−1, 1) |

---

## 🛠️ Key Python Libraries Used Across Labs

```python
# Data
import pandas as pd, numpy as np

# Visualization (Lec 3–4, Labs 2–4)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Preprocessing (Lab 4–5)
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

# Classification (Labs 9–10, 12)
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, ConfusionMatrixDisplay, roc_auc_score, RocCurveDisplay)

# Clustering (Labs 10–11)
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA

# Association Rules (Labs 6–8)
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

# PySpark (Lab 12)
from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth
from pyspark.ml.clustering import KMeans as SparkKMeans
from pyspark.ml.feature import VectorAssembler
```

---

## 📝 Report Structure (What Prof Expects)

Based on Lab submissions (Lab 3, Lab 5, Lab 9, Lab 10, Lab 11, Lab 12 reports studied):

### 1. Descriptive Analysis
- Dataset overview: source, shape, attribute types, data dictionary
- KDD Phase explicitly stated
- Missing values, duplicates report
- Descriptive statistics table (mean, median, mode, std, skewness)
- **At least 5–6 visualizations**: histogram, box plot, scatter, bar, heatmap, pareto/doughnut/radar
- **Every plot → 2–3 sentence inference** (this is non-negotiable based on past labs)
- Correlation matrix with top pairs highlighted

### 2. Predictive Analysis
- Classification / regression problem statement
- Preprocessing steps (normalize, encode, handle missing — state logic for each)
- Train/test split ratio stated
- Multiple models compared (minimum 2–3)
- Metrics table: Accuracy, Precision, Recall, F1, AUC
- Confusion matrix screenshot
- ROC curve (if binary)
- Best model justified

### 3. Big Data Analysis
- Why big data approach (volume justification)
- PySpark or distributed algorithm used
- Performance comparison: sequential vs parallel
- Association rules or cluster analysis output
- Tables + screenshots of output

### 4. Conclusion
- Key findings per section
- Domain insights / business implications
- Limitations
- Future scope

> [!IMPORTANT]
> From Lab 9 report pattern: **Executive Summary** at top — 3–4 bullet key takeaways before diving in. This impresses immediately.

> [!TIP]
> From Lab 11 report: Prof rewards breadth — testing **multiple variants** of an algorithm (e.g., different linkage methods, different eps values) with comparison tables earns more marks than a single run.

---

## ⚠️ Common Pitfalls (Learned from Lab History)

> [!WARNING]
> - **Class imbalance:** Bank Marketing was 88.7% negative. Never report only accuracy — always F1 + AUC
> - **Dense datasets in Apriori/FP-Growth:** Cap `max_len=2` to avoid combinatorial explosion (chess dataset: 37 items/tx)
> - **Overfitting:** Unconstrained DT → 100% train, ~53% test F1. Always tune `max_depth`
> - **Missing inferences:** Every plot without inference = marks lost. Write inference inline in notebook as markdown

> [!CAUTION]
> - **High-nullity columns:** Drop attributes with >90–95% missing (Smart City: emergency columns ~97.6% missing)
> - **PySpark local mode:** Always use `master("local[*]")` and wrap in try/except for resource limits
> - **Saving outputs:** Don't rely on re-running — save figures with `plt.savefig()` as you go

---

*📌 Tomorrow: share the question paper → I'll divide it into phases with time estimates.*
