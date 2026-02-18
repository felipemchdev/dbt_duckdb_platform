select
    'fct_orders is empty' as validation_error
where not exists (
    select 1
    from {{ ref('fct_orders') }}
)
