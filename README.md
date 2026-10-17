# Instacart Customer Ordering Behavior

> Versión en español: [LEEME.md](LEEME.md)

An exploratory data analysis of **Instacart**, a grocery delivery platform, to understand **when customers order, how often they come back, and which products they buy and reorder**.

The project cleans five related tables (almost 480,000 orders and 4.5 million ordered items), interprets each anomaly before treating it, and then studies ordering times, customer frequency, and product popularity. Key results: orders concentrate **between 10 a.m. and 4 p.m. and on Sundays and Mondays**; the most common gap between orders is **7 days**; **59% of ordered items are reorders**; and the most popular products are **fresh produce, led by bananas**.

---

# Business Context

Instacart customers place grocery orders in the app and get them delivered. Understanding ordering behavior helps the business to:

* Plan delivery capacity for the busiest days and hours.
* Design reminders and recommendations based on recurring purchases.
* Know which products drive customer loyalty.

The analysis answers three groups of questions:

| Group | Questions |
| --- | --- |
| **A. Ordering time** | At what hours and on which days do people order? How long do they wait between orders? |
| **B. Customers and products** | Do Wednesdays and Saturdays differ? How many orders does each customer place? Which products are the most popular? |
| **C. Baskets and reorders** | How many items are in an order? Which products are reordered most? What share of each product and each customer's purchases are reorders? Which products go into the cart first? |

---

# Key Concepts

| Term | Meaning |
| --- | --- |
| Order | One purchase by one customer; it can contain many products |
| `order_number` | How many orders the customer has placed so far (1 = first order) |
| `days_since_prior_order` | Days since the customer's previous order; capped at 30 |
| `add_to_cart_order` | Position in which a product was added to the cart |
| Reorder | A product the customer had already bought before (`reordered = 1`) |
| Reorder rate | Reordered items divided by total items, by product or by customer |

---

# Dataset

| File | Rows | Description |
| --- | ---: | --- |
| `data/instacart_orders.csv` | 478,967 | One row per order: customer, order number, day of week, hour, and days since the prior order |
| `data/order_products.csv` | 4,545,007 | One row per product in an order: cart position and reorder flag |
| `data/products.csv` | 49,694 | Product catalog: name, aisle, and department |
| `data/aisles.csv` | 134 | Aisle names |
| `data/departments.csv` | 21 | Department names |

* The files use `;` as separator.
* `order_dow` uses 0 = Sunday.
* The dataset is a reduced version of the original Instacart data, with missing values and duplicates added on purpose, while keeping the original distributions.

**Data source.** The datasets were provided by **TripleTen** as part of its Data Science Bootcamp, based on public Instacart data, and are included in this repository for educational and reproducibility purposes.

---

# Project Workflow

```text
5 tables (orders, order_products, products, aisles, departments)
            │
            ▼
1. Data description: structure, types, missing values
            │
            ▼
2. Preprocessing: duplicates and missing values, interpreted before treating them
            │
            ▼
3. Exploratory analysis
   ├── [A] Ordering time: hour, day of week, days between orders
   ├── [B] Wednesday vs Saturday, orders per customer, top 20 products
   └── [C] Items per order, reorders by product and customer, first items in the cart
```

---

# 1. Data Preparation

## Duplicates

| Table | Finding | Decision |
| --- | --- | --- |
| `orders` | 15 fully duplicated rows, **all on Wednesday at 2 a.m.** (probably a system error at that time) | Removed |
| `orders` | Repeated `user_id` values | Kept: a customer can place many orders; `order_id` has no duplicates |
| `products` | Same product name with different `product_id` | Kept: `product_id` is the unique key |
| `aisles`, `departments`, `order_products` | No duplicates, also after normalizing names | — |

## Missing Values

| Column | Missing | What they mean | Treatment |
| --- | ---: | --- | --- |
| `days_since_prior_order` | 28,819 | After removing duplicates, all 28,817 are **first orders** (`order_number = 1`) | Replaced with **−1** to tell first orders apart from real waiting times |
| `product_name` | 1,258 | All belong to aisle 100 and department 21, both named **"missing"** | Replaced with `"Unknown"` |
| `add_to_cart_order` | 836 | They come from **70 orders with more than 64 products** (65 to 127); the cart position seems to be recorded only up to 64 | Replaced with **999** (outside the real 1–64 range) and the column converted to integer |

Product, aisle, and department names were normalized (trimmed, same case) to check for hidden duplicates.

---

# 2. Data Analysis

## [A] Ordering Time

* **Hours:** activity concentrates **between 10 a.m. and 4 p.m.**, with two slight peaks around 11 a.m. and 3 p.m. and a small dip at noon. The quietest hours are 3–5 a.m.
* **Days:** **Sunday** (57,661 customers) and **Monday** (56,479) are the busiest days; **Thursday** (44,281) is the quietest.
* **Days between orders:** most repeat orders come **1 to 9 days** after the previous one. The most common gap is **7 days**, with smaller peaks at **14, 21, and 28 days**, which suggests weekly shopping routines. The value 30 is very frequent, but it probably groups every wait of 30 days or more.

## [B] Customers and Products

**Wednesday vs Saturday.** The hourly distributions are very similar: no hour differs by more than 1 percentage point. Wednesday has a slightly larger share of orders at 9–10 a.m. and 6–8 p.m., and Saturday at 12–2 p.m.

**Orders per customer.**

| Orders placed | Customers |
| ---: | ---: |
| 1 | 55,357 |
| 2 | 36,508 |
| 3 | 21,547 |
| 4 | 13,498 |
| 5 or more | 30,527 (19%) |

The number of customers drops as the number of orders grows, but almost one in five customers placed 5 or more orders (up to 28).

**Top 20 products.** Bananas lead (single bananas, then bags of organic bananas), followed by organic strawberries, baby spinach, and avocados. **19 of the 20 are fruits or vegetables** (the exception is organic whole milk) and **14 of the 20 are organic**.

## [C] Baskets and Reorders

* **Items per order:** mean 10.1, median 8, and most frequent value 5. Half of the orders have between 5 and 14 items; a few large orders reach 127 items.
* **Most reordered products:** **19 of the 20** most popular products are also among the 20 most reordered. Organic grape tomatoes appear only among the most popular, and organic half & half only among the most reordered.
* **Reorder rate by product:** goes from 0 to 1; 1,809 products were always reordered.
* **Reorder rate by customer:** also from 0 to 1; 8,102 customers only bought products they had bought before.
* **First items in the cart:** bananas are again first (15,562 and 11,026 times), followed by organic whole milk and organic strawberries. **12 products** appear in all three lists: most popular, most reordered, and first added to the cart.

---

# Conclusions

1. **Anomalies had a meaning.** Missing waiting times were first orders, missing product names belonged to a "missing" category, and missing cart positions belonged to orders with more than 64 items. Understanding them avoided wrong imputations.

2. **Customers follow routines**: orders concentrate in daytime hours and at the start of the week, and the most common gap between orders is exactly one week.

3. **Loyalty is high**: 59% of ordered items are reorders, and the most popular products are also the most reordered.

4. **Fresh produce drives the business**: bananas, berries, avocados, and leafy greens lead in popularity, reorders, and first place in the cart.

## Business Interpretation

* **Logistics:** reinforce delivery capacity on Sundays and Mondays between 10 a.m. and 4 p.m.
* **Reminders:** a weekly reminder fits the most common ordering cycle.
* **Recommendations:** products that are frequently reordered or added first, such as bananas, milk, and berries, are good candidates for "buy again" suggestions.

## Next Steps

* Segment customers by ordering frequency and basket size.
* Analyze which departments and aisles have the highest reorder rates.
* Build a model to predict which products a customer will reorder.

---

# Project Structure

```text
food-delivery-company-visual-statistic-analysis/
│
├── data/
│   ├── aisles.csv
│   ├── departments.csv
│   ├── instacart_orders.csv
│   ├── order_products.csv
│   └── products.csv
│
├── notebooks/
│   └── food_delivery_company_visual_statistic_analysis.ipynb
│
├── src/
│   └── funciones_personales.py
│
├── .gitignore
├── environment.yml
├── requirements.txt
├── LEEME.md
└── README.md
```

`src/funciones_personales.py` contains helper functions to find missing values (`mostrar_nan`) and duplicates (`mostrar_dupli`, `filas_dup`).

---

# Installation

Clone the repository:

```bash
git clone https://github.com/pablo-vc87/food-delivery-company-visual-statistic-analysis.git

cd food-delivery-company-visual-statistic-analysis
```

## Option 1: Conda

```bash
conda env create -f environment.yml
conda activate food-delivery-analysis
jupyter notebook
```

## Option 2: pip

Create and activate a virtual environment, then:

```bash
pip install -r requirements.txt
jupyter notebook
```

Open `notebooks/food_delivery_company_visual_statistic_analysis.ipynb` and run all cells.

---

# Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Jupyter Notebook

---

# Skills Demonstrated

* Data quality assessment across related tables
* Interpreting missing values and duplicates before treating them
* Joins between transactional and catalog tables
* Grouping and aggregation of large datasets (4.5 million rows)
* Data visualization with bar charts and histograms
* Reorder rate analysis by product and by customer
* Translating behavior patterns into logistics and marketing ideas

---

## Author

**Pablo Andrés Vázquez Calva**

Data Scientist

GitHub: https://github.com/pablo-vc87

LinkedIn: https://www.linkedin.com/in/pablo-avc/
