import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import re

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

# Load raw CSV
df = pd.read_csv("data/amazon.csv")
print(f"Loaded {len(df)} rows")

# Clean price columns
def clean_price(val):
    if pd.isna(val): return None
    return float(re.sub(r'[₹,]', '', str(val)).strip())

df['discounted_price'] = df['discounted_price'].apply(clean_price)
df['actual_price']     = df['actual_price'].apply(clean_price)

# Clean discount percentage
df['discount_percentage'] = df['discount_percentage'].str.replace('%','').str.strip()
df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')

# Clean rating and rating_count
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = df['rating_count'].str.replace(',','').str.strip()
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce').fillna(0).astype(int)

# Parse category hierarchy into separate levels
cat_split = df['category'].str.split('|', expand=True)
df['category_l1'] = cat_split[0]
df['category_l2'] = cat_split[1]
df['category_l3'] = cat_split[2]
df['category_l4'] = cat_split[3]
df['category_l5'] = cat_split[4]

# Deduplicate products, keeping the one with highest rating_count
df = df.sort_values('rating_count', ascending=False)
df_products = df.drop_duplicates(subset='product_id', keep='first')
print(f"Unique products: {len(df_products)}")

# Load raw staging table
df.to_sql('raw_amazon', engine, if_exists='replace', index=False)
print("Loaded raw_amazon")

# Build dim_categories
cats = df[['category_l1','category_l2','category_l3','category_l4','category_l5']].drop_duplicates()
cats = cats.reset_index(drop=True)
cats.index.name = 'category_id'
cats = cats.reset_index()
cats.to_sql('dim_categories', engine, if_exists='replace', index=False)
print("Loaded dim_categories")

# Build dim_products
dim_products = df_products[['product_id','product_name','about_product','img_link','product_link']].copy()
dim_products.to_sql('dim_products', engine, if_exists='replace', index=False)
print("Loaded dim_products")

# Build fct_product_metrics
cat_lookup = cats.set_index(
    ['category_l1','category_l2','category_l3','category_l4','category_l5']
)['category_id']

df_products = df_products.copy()
df_products['category_id'] = df_products.set_index(
    ['category_l1','category_l2','category_l3','category_l4','category_l5']
).index.map(cat_lookup).values

fct = df_products[[
    'product_id', 'category_id',
    'discounted_price', 'actual_price',
    'discount_percentage', 'rating', 'rating_count'
]].copy()
fct['savings']     = fct['actual_price'] - fct['discounted_price']
fct['value_score'] = (fct['rating'] * fct['rating_count']).round(0)

fct.to_sql('fct_product_metrics', engine, if_exists='replace', index=False)
print("Loaded fct_product_metrics")

print("ETL complete. Tables created: raw_amazon, dim_products, dim_categories, fct_product_metrics")