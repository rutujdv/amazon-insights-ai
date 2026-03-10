with source as (
    select * from {{ source('amazon_insights', 'raw_amazon') }}
),

cleaned as (
    select
        product_id,
        product_name,
        category,
        discounted_price,
        actual_price,
        discount_percentage,
        rating,
        rating_count,
        about_product,
        img_link,
        product_link,
        category_l1,
        category_l2,
        category_l3,
        category_l4,
        category_l5
    from source
    where product_id is not null
    and rating is not null
    and discounted_price is not null
)

select * from cleaned