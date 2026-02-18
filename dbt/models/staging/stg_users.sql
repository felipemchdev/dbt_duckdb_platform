with source_data as (
    select *
    from {{ source('raw', 'raw_users') }}
)

select
    cast(user_id as integer) as user_id,
    lower(trim(email)) as email,
    cast(created_at as timestamp) as created_at,
    upper(trim(country)) as country
from source_data
