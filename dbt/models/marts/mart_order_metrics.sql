select
    count(*) as total_orders,
    cast(round(sum(amount), 2) as decimal(18,2)) as total_revenue,
    sum(case when status = 'paid' then 1 else 0 end) as paid_orders,
    sum(case when status = 'canceled' then 1 else 0 end) as canceled_orders
from {{ ref('fct_orders') }}
