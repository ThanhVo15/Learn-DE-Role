select
    trade_id,
    security_id,
    trade_date,
    price,
    volume
from {{ source('raw_data', 'trades') }}