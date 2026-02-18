select
    o.order_id,
    o.user_id,
    o.amount,
    o.status,
    o.created_at,
    cast(o.created_at as date) as order_date
from {{ ref('stg_orders') }} as o
inner join {{ ref('dim_users') }} as u
    on o.user_id = u.user_id
