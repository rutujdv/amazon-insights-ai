with stg as (
    select * from {{ ref('stg_amazon_raw') }}
),

unique_cats as (
    select distinct
        category_l1,
        category_l2,
        category_l3,
        category_l4,
        category_l5
    from stg
)

select
    row_number() over (order by category_l1, category_l2, category_l3) - 1 as category_id,
    category_l1,
    category_l2,
    category_l3,
    category_l4,
    category_l5
from unique_cats