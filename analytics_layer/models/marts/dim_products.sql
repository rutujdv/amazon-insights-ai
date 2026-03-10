with stg as (
    select * from {{ ref('stg_amazon_raw') }}
),

deduped as (
    select
        product_id,
        product_name,
        about_product,
        img_link,
        product_link,
        row_number() over (
            partition by product_id
            order by rating_count desc
        ) as row_num
    from stg
)

select
    product_id,
    product_name,
    about_product,
    img_link,
    product_link
from deduped
where row_num = 1