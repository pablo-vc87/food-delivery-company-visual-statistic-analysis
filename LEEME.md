# Comportamiento de Pedidos de Clientes de Instacart

> English version: [README.md](README.md)

Análisis exploratorio de datos de **Instacart**, una plataforma de entrega de víveres, para entender **cuándo hacen pedidos los clientes, cada cuánto regresan y qué productos compran y vuelven a pedir**.

El proyecto limpia cinco tablas relacionadas (casi 480,000 pedidos y 4.5 millones de artículos pedidos), interpreta cada anomalía antes de tratarla y después estudia los horarios de pedido, la frecuencia de los clientes y la popularidad de los productos. Resultados clave: los pedidos se concentran **entre las 10 a.m. y las 4 p.m. y los domingos y lunes**; el intervalo más común entre pedidos es de **7 días**; **el 59% de los artículos pedidos son repeticiones**; y los productos más populares son **frutas y verduras frescas, encabezadas por el plátano**.

---

# Contexto de Negocio

Los clientes de Instacart hacen pedidos de víveres en la aplicación y los reciben a domicilio. Entender su comportamiento ayuda al negocio a:

* Planear la capacidad de entrega para los días y horas de mayor demanda.
* Diseñar recordatorios y recomendaciones basados en compras recurrentes.
* Saber qué productos generan lealtad.

El análisis responde tres grupos de preguntas:

| Grupo | Preguntas |
| --- | --- |
| **A. Horario de los pedidos** | ¿A qué horas y qué días piden las personas? ¿Cuánto esperan entre pedidos? |
| **B. Clientes y productos** | ¿Hay diferencias entre miércoles y sábado? ¿Cuántos pedidos hace cada cliente? ¿Cuáles son los productos más populares? |
| **C. Carritos y repeticiones** | ¿Cuántos artículos tiene un pedido? ¿Qué productos se vuelven a pedir más? ¿Qué proporción de las compras de cada producto y de cada cliente son repeticiones? ¿Qué productos se agregan primero al carrito? |

---

# Conceptos Clave

| Término | Significado |
| --- | --- |
| Pedido | Una compra de un cliente; puede contener muchos productos |
| `order_number` | Cuántos pedidos lleva el cliente (1 = primer pedido) |
| `days_since_prior_order` | Días desde el pedido anterior del cliente; tiene un tope de 30 |
| `add_to_cart_order` | Posición en la que se agregó un producto al carrito |
| Repetición (reorder) | Un producto que el cliente ya había comprado antes (`reordered = 1`) |
| Tasa de repetición | Artículos repetidos entre el total de artículos, por producto o por cliente |

---

# Dataset

| Archivo | Filas | Descripción |
| --- | ---: | --- |
| `data/instacart_orders.csv` | 478,967 | Una fila por pedido: cliente, número de pedido, día de la semana, hora y días desde el pedido anterior |
| `data/order_products.csv` | 4,545,007 | Una fila por producto en un pedido: posición en el carrito e indicador de repetición |
| `data/products.csv` | 49,694 | Catálogo de productos: nombre, pasillo y departamento |
| `data/aisles.csv` | 134 | Nombres de los pasillos |
| `data/departments.csv` | 21 | Nombres de los departamentos |

* Los archivos usan `;` como separador.
* `order_dow` usa 0 = domingo.
* El dataset es una versión reducida de los datos originales de Instacart, a la que se le agregaron a propósito valores ausentes y duplicados, conservando las distribuciones originales.

**Fuente de los datos.** Los datasets fueron proporcionados por **TripleTen** como parte de su Bootcamp de Data Science, a partir de datos públicos de Instacart, y se incluyen en este repositorio con fines educativos y de reproducibilidad.

---

# Flujo del Proyecto

```text
5 tablas (orders, order_products, products, aisles, departments)
            │
            ▼
1. Descripción de los datos: estructura, tipos, valores ausentes
            │
            ▼
2. Preprocesamiento: duplicados y valores ausentes, interpretados antes de tratarlos
            │
            ▼
3. Análisis exploratorio
   ├── [A] Horario: hora, día de la semana, días entre pedidos
   ├── [B] Miércoles vs sábado, pedidos por cliente, 20 productos principales
   └── [C] Artículos por pedido, repeticiones por producto y cliente, primeros artículos del carrito
```

---

# 1. Preparación de los Datos

## Duplicados

| Tabla | Hallazgo | Decisión |
| --- | --- | --- |
| `orders` | 15 filas totalmente duplicadas, **todas de miércoles a las 2 a.m.** (probablemente un error del sistema a esa hora) | Eliminadas |
| `orders` | Valores repetidos de `user_id` | Se conservan: un cliente puede hacer muchos pedidos; `order_id` no tiene duplicados |
| `products` | Mismo nombre de producto con distinto `product_id` | Se conservan: `product_id` es la clave única |
| `aisles`, `departments`, `order_products` | Sin duplicados, también después de normalizar los nombres | — |

## Valores Ausentes

| Columna | Ausentes | Qué significan | Tratamiento |
| --- | ---: | --- | --- |
| `days_since_prior_order` | 28,819 | Después de quitar duplicados, los 28,817 son **primeros pedidos** (`order_number = 1`) | Se reemplazaron por **−1** para distinguir los primeros pedidos de los tiempos de espera reales |
| `product_name` | 1,258 | Todos pertenecen al pasillo 100 y al departamento 21, ambos llamados **"missing"** | Se reemplazaron por `"Unknown"` |
| `add_to_cart_order` | 836 | Vienen de **70 pedidos con más de 64 productos** (de 65 a 127); al parecer la posición en el carrito solo se registró hasta 64 | Se reemplazaron por **999** (fuera del rango real 1–64) y la columna se convirtió a entero |

Los nombres de productos, pasillos y departamentos se normalizaron (sin espacios extra y con las mismas mayúsculas) para buscar duplicados ocultos.

---

# 2. Análisis de los Datos

## [A] Horario de los Pedidos

* **Horas:** la actividad se concentra **entre las 10 a.m. y las 4 p.m.**, con dos picos ligeros alrededor de las 11 a.m. y las 3 p.m. y una pequeña baja al mediodía. Las horas más tranquilas son de 3 a 5 a.m.
* **Días:** el **domingo** (57,661 clientes) y el **lunes** (56,479) son los días con más actividad; el **jueves** (44,281) es el más tranquilo.
* **Días entre pedidos:** la mayoría de los pedidos repetidos llega **de 1 a 9 días** después del anterior. El intervalo más común es de **7 días**, con picos menores a los **14, 21 y 28 días**, lo que sugiere rutinas de compra semanales. El valor 30 es muy frecuente, pero probablemente agrupa todas las esperas de 30 días o más.

## [B] Clientes y Productos

**Miércoles vs sábado.** Las distribuciones por hora son muy parecidas: ninguna hora difiere en más de 1 punto porcentual. El miércoles tiene una proporción algo mayor de pedidos a las 9–10 a.m. y de 6 a 8 p.m., y el sábado entre las 12 y las 2 p.m.

**Pedidos por cliente.**

| Pedidos realizados | Clientes |
| ---: | ---: |
| 1 | 55,357 |
| 2 | 36,508 |
| 3 | 21,547 |
| 4 | 13,498 |
| 5 o más | 30,527 (19%) |

El número de clientes baja conforme aumenta el número de pedidos, pero casi uno de cada cinco clientes hizo 5 pedidos o más (hasta 28).

**Los 20 productos principales.** Encabezan los plátanos (plátano por unidad y después la bolsa de plátanos orgánicos), seguidos por fresas orgánicas, espinaca baby y aguacates. **19 de los 20 son frutas o verduras** (la excepción es la leche entera orgánica) y **14 de los 20 son orgánicos**.

## [C] Carritos y Repeticiones

* **Artículos por pedido:** media de 10.1, mediana de 8 y valor más frecuente de 5. La mitad de los pedidos tiene entre 5 y 14 artículos; algunos pedidos grandes llegan a 127.
* **Productos que más se vuelven a pedir:** **19 de los 20** productos más populares también están entre los 20 más repetidos. Los jitomates uva orgánicos solo aparecen entre los más populares, y la crema half & half orgánica solo entre los más repetidos.
* **Tasa de repetición por producto:** va de 0 a 1; 1,809 productos siempre se volvieron a pedir.
* **Tasa de repetición por cliente:** también va de 0 a 1; 8,102 clientes solo compraron productos que ya habían comprado antes.
* **Primeros artículos del carrito:** los plátanos vuelven a ir primero (15,562 y 11,026 veces), seguidos por la leche entera orgánica y las fresas orgánicas. **12 productos** aparecen en las tres listas: más populares, más repetidos y primeros en el carrito.

---

# Conclusiones

1. **Las anomalías tenían un significado.** Los tiempos de espera faltantes eran primeros pedidos, los nombres faltantes pertenecían a una categoría "missing" y las posiciones faltantes en el carrito eran de pedidos con más de 64 artículos. Entenderlas evitó imputaciones equivocadas.

2. **Los clientes siguen rutinas**: los pedidos se concentran en horario diurno y al inicio de la semana, y el intervalo más común entre pedidos es exactamente una semana.

3. **La lealtad es alta**: el 59% de los artículos pedidos son repeticiones, y los productos más populares también son los más repetidos.

4. **Las frutas y verduras frescas impulsan el negocio**: plátanos, frutos rojos, aguacates y hojas verdes encabezan en popularidad, repeticiones y primer lugar en el carrito.

## Interpretación de Negocio

* **Logística:** reforzar la capacidad de entrega los domingos y lunes entre las 10 a.m. y las 4 p.m.
* **Recordatorios:** un recordatorio semanal coincide con el ciclo de pedido más común.
* **Recomendaciones:** los productos que más se repiten o se agregan primero, como plátanos, leche y frutos rojos, son buenos candidatos para sugerencias de "volver a comprar".

## Siguientes Pasos

* Segmentar a los clientes por frecuencia de pedido y tamaño del carrito.
* Analizar qué departamentos y pasillos tienen las mayores tasas de repetición.
* Construir un modelo que prediga qué productos volverá a pedir cada cliente.

---

# Estructura del Proyecto

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

`src/funciones_personales.py` contiene funciones auxiliares para encontrar valores ausentes (`mostrar_nan`) y duplicados (`mostrar_dupli`, `filas_dup`).

---

# Instalación

Clona el repositorio:

```bash
git clone https://github.com/pablo-vc87/food-delivery-company-visual-statistic-analysis.git

cd food-delivery-company-visual-statistic-analysis
```

## Opción 1: Conda

```bash
conda env create -f environment.yml
conda activate food-delivery-analysis
jupyter notebook
```

## Opción 2: pip

Crea y activa un entorno virtual y después:

```bash
pip install -r requirements.txt
jupyter notebook
```

Abre `notebooks/food_delivery_company_visual_statistic_analysis.ipynb` y ejecuta todas las celdas.

---

# Tecnologías

* Python
* Pandas
* NumPy
* Matplotlib
* Jupyter Notebook

---

# Habilidades Demostradas

* Evaluación de la calidad de datos en tablas relacionadas
* Interpretación de valores ausentes y duplicados antes de tratarlos
* Uniones entre tablas transaccionales y de catálogo
* Agrupación y agregación de datos grandes (4.5 millones de filas)
* Visualización de datos con gráficos de barras e histogramas
* Análisis de tasas de repetición por producto y por cliente
* Traducción de patrones de comportamiento a ideas de logística y marketing

---

## Autor

**Pablo Andrés Vázquez Calva**

Data Scientist

GitHub: https://github.com/pablo-vc87

LinkedIn: https://www.linkedin.com/in/pablo-avc/
