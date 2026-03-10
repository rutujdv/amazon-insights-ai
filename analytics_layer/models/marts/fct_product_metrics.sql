with stg as (
    select * from {{ ref('stg_amazon_raw') }}
),

dim_cats as (
    select * from {{ ref('dim_categories') }}
),

joined as (
    select
        s.product_id,
        c.category_id,
        s.discounted_price,
        s.actual_price,
        s.discount_percentage,
        s.rating,
        s.rating_count,
        s.actual_price - s.discounted_price   as savings,
        round((s.rating * s.rating_count)::numeric, 0)   as value_score
    from stg s
    left join dim_cats c
        on  s.category_l1 = c.category_l1
        and s.category_l2 = c.category_l2
        and s.category_l3 = c.category_l3
        and s.category_l4 = c.category_l4
        and s.category_l5 = c.category_l5
)

select * from joined