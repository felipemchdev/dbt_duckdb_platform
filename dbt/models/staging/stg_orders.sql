with source_data as (
    select *
    from {{ source('raw', 'raw_orders') }}
)

select
    cast(order_id as integer) as order_id,
    cast(user_id as integer) as user_id,
    cast(amount as decimal(18,2)) as amount,
    lower(trim(status)) as status,
    cast(created_at as timestamp) as created_at
from source_data
