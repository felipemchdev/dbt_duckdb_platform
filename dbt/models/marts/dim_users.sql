select
    user_id,
    email,
    country,
    created_at as user_created_at
from {{ ref('stg_users') }}
