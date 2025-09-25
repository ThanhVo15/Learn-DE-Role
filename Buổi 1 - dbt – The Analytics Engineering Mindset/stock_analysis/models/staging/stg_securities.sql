select
    id as security_id,
    ticker_symbol,
    company_name
from {{ source( 'raw_data', 'securities')}}