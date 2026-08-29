# Food Delivery Company Visual Statistical Analysis

## Project Overview

This project analyzes customer ordering behavior for **Instacart**, a grocery delivery platform similar to other on-demand delivery services. The analysis uses a modified version of the Instacart dataset containing a reduced sample of the original data, along with introduced missing values and duplicated records.

The project follows a structured workflow:

1. **Data Description** — inspect the datasets, their structure, data types, and missing values.
2. **Data Preprocessing** — identify and handle missing values, duplicated records, and data inconsistencies.
3. **Exploratory Data Analysis (EDA)** — investigate ordering patterns, customer behavior, product popularity, and reordering habits.

The main objective is to transform the raw transactional data into reliable information that can support business decisions related to recommendations, customer retention, logistics, and operational planning.

## Repository Structure

```text
food-delivery-company-visual-statistic-analysis/
│
├── data/
│   ├── instacart_orders.csv
│   ├── products.csv
│   ├── order_products.csv
│   ├── aisles.csv
│   └── departments.csv
│
├── src/
│   └── funciones_personales.py
│
├── notebooks/
│   └── food_delivery_company_visual_statistic_analysis.ipynb
│
├── requirements.txt
├── environment.yml
└── README.md
```

## Dataset

The project uses five related CSV files:

| File | Description |
|---|---|
| `instacart_orders.csv` | Order-level information, including customer, order number, day, hour, and time since the previous order. |
| `products.csv` | Product catalog containing product, aisle, and department identifiers. |
| `order_products.csv` | Products included in each order, their cart position, and whether they were reordered. |
| `aisles.csv` | Grocery aisle identifiers and names. |
| `departments.csv` | Grocery department identifiers and names. |

The CSV files use `;` as the field separator.

## Tools and Technologies

- **Python**
- **Pandas** — data loading, cleaning, transformation, aggregation, and analysis
- **NumPy** — numerical operations and validation
- **Matplotlib** — data visualization
- **Jupyter Notebook** — analysis and presentation
- **Custom Python functions** — reusable analysis and visualization utilities stored in `src/funciones_personales.py`

## Analysis Workflow

### 1. Data Description

The five datasets were loaded and inspected using methods such as `.info()` and `.isna().sum()`.

The initial inspection identified:

- `instacart_orders.csv`: 478,967 rows and 6 columns.
- `products.csv`: 49,694 rows and 4 columns.
- `order_products.csv`: 4,545,007 rows and 4 columns.
- `aisles.csv`: 134 rows and 2 columns.
- `departments.csv`: 21 rows and 2 columns.

Missing values were found in:

- `instacart_orders.days_since_prior_order`: 28,819 values.
- `products.product_name`: 1,258 values.
- `order_products.add_to_cart_order`: 836 values.

No missing values were identified in the `aisles` or `departments` tables.

### 2. Data Preprocessing

The preprocessing stage focused on understanding the meaning of anomalies before deciding how to treat them.

#### Orders

Fifteen duplicated rows were identified in the orders table. They occurred in the same Wednesday-at-2:00-a.m. time period and were analyzed in context before removal.

Missing values in `days_since_prior_order` were associated with first orders (`order_number == 1`). They were represented as `-1` to distinguish first orders from subsequent orders.

The 15 confirmed duplicate rows were removed using `drop_duplicates()` and the index was reset.

The repetition of `user_id` values was not treated as an error because a customer can naturally place multiple orders. The combination of `user_id` and `order_id` was checked to validate order uniqueness.

#### Products

The `product_name` column contained 1,258 missing values. These records were associated with `aisle_id = 100` and `department_id = 21`, which correspond to the missing-reference categories in the provided dataset.

A new product-name field was used during the analysis, with missing names represented as `"Unknown"`.

Product names were also converted to uppercase to facilitate duplicate-name analysis. Multiple products can share the same name because `product_id` is the unique product identifier.

#### Order Products

The `add_to_cart_order` column contained 836 missing values. The column was converted from `float64` to `int64`, and missing positions were represented by `999` to indicate an undefined cart position.

#### Aisles and Departments

No missing values or duplicate records requiring correction were found in these tables. Additional normalized text columns were used to validate the uniqueness of aisle and department names.

## Exploratory Data Analysis

The EDA investigated three main areas: order timing, customer purchasing behavior, and product/reordering behavior.

### Ordering Time

The values of `order_hour_of_day` and `order_dow` were checked to ensure that they fell within their expected ranges.

The analysis found a bimodal pattern in ordering activity:

- One major peak occurs around **9–10 a.m.**
- Another major peak occurs around **2–3 p.m.**
- The lowest activity occurs during the early morning hours.

Orders are particularly concentrated on **Sunday and Monday**, while Thursday has comparatively lower activity.

The distribution of days between orders is concentrated primarily between **1 and 9 days**, with additional recurring peaks around **7, 14, 21, and 28 days**. The dataset limits interpretation of the 30-day value because orders beyond 30 days may be grouped into the 30-day category.

### Wednesday vs. Saturday

The hourly distributions differ between Wednesday and Saturday.

Wednesday shows higher activity during several morning hours and again during the evening, while Saturday displays stronger activity during overnight/early-morning hours, late morning, afternoon, and late evening.

### Customer Order Frequency

The number of orders per customer follows a decreasing distribution: as the number of orders increases, fewer customers are represented.

The analysis found more than 50,000 customers with a single order, while relatively few customers placed five or more orders.

### Most Popular Products

The 20 most frequently ordered products were identified by combining order and product information.

According to the project analysis, the leading products were predominantly organic fruits and vegetables, with bananas occupying the top positions.

### Reordering Behavior

Reordering was analyzed using the `reordered` indicator.

The analysis distinguished between:

- **Raw reorder counts** — the total number of times a product was reordered.
- **Reorder rate** — the proportion of a product's orders that were reorders.

Nineteen of the 20 most frequently ordered products also appeared among the 20 most frequently reordered products.

At the product level, reorder proportions ranged from 0 to 1, with 1,809 products showing a reorder proportion of 1 in the analyzed data.

At the customer level, the reorder proportion was calculated as:

```text
reordered items / total items ordered
```

This customer-level measure also ranged from 0 to 1, with 8,102 customers showing a proportion of 1.

### First Items Added to the Cart

The analysis identified the products most frequently placed first in customers' carts.

Bananas, both individually and in bags, were among the leading first-added products. Twelve products appeared simultaneously among the most popular, most reordered, and most frequently first-added products.

## Business Insights

The analysis suggests several practical applications for an online grocery delivery business:

1. **Personalized recommendations and reminders**  
   Products with strong reorder behavior and customers with recurring purchase patterns can be used to support personalized recommendations and purchase reminders.

2. **Operational and logistics planning**  
   Concentrating resources around the days and hours with higher order volumes may help improve operational capacity, reduce bottlenecks, and support delivery performance.

3. **Future predictive analysis**  
   The cleaned dataset provides a foundation for future work involving demand forecasting, customer segmentation, product recommendation systems, and predictive modeling.

## Key Takeaways

The project demonstrates the importance of connecting data cleaning decisions with the meaning of the underlying business process.

The main findings include:

- Customers display recurring purchasing routines.
- Order activity is concentrated in specific days and hours.
- Reordering is common for many products.
- Some products consistently appear among popular, reordered, and first-added items.
- Missing values can contain meaningful business information and should be interpreted before being imputed.
- Duplicate records should be investigated in context rather than removed automatically.

Overall, the analysis shows how a structured process—from data inspection and preprocessing to exploratory analysis—can reveal actionable patterns in digital commerce data.

## How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd food-delivery-company-visual-statistic-analysis
```

### 2. Create the Conda environment

```bash
conda env create -f environment.yml
```

Activate it with:

```bash
conda activate food-delivery-analysis
```

### 3. Alternatively, install the Python dependencies with pip

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

```bash
jupyter notebook
```

Open:

```text
notebooks/food_delivery_company_visual_statistic_analysis.ipynb
```

The notebook expects the dataset files to remain in the repository's `data/` directory and the helper module in `src/`.

## Notes

The analysis is based on the modified Instacart dataset provided for the project. The dataset intentionally contains a reduced number of records and introduced missing values and duplicates while preserving the general distributions of the original data.

The conclusions in this repository describe patterns observed in this provided dataset and should not automatically be generalized to the entire Instacart customer population.
