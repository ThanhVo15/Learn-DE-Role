-- trade_id,security_id,trade_date,price,volume
-- 1,101,2023-10-26,150.50,100
-- 2,102,2023-10-26,200.00,50
-- 3,101,2023-10-27,152.00,75
-- 4,103,2023-10-27,55.25,200

-- id,ticker_symbol,company_name
-- 101,AAPL,Apple Inc.
-- 102,GOOGL,Alphabet Inc.
-- 103,MSFT,Microsoft Corporation

{{
    config(
        materialized = 'incremental',
        unique_key = 'trade_date'
    )
}}

with trades_with_value as (
    select
        a.trade_date,
        b.ticker_symbol,
        a.volume,
        a.price * a.volume as trade_value
    from {{ ref('stg_trades') }} as a
    join {{ ref('stg_securities') }} as b
        on a.security_id = b.security_id
)
select
    trade_date,
    ticker_symbol,
    sum(volume) as total_volume,
    sum(trade_value) as total_trade_value
from trades_with_value
group by trade_date, ticker_symbol
order by trade_date, ticker_symbol

{% if is_incremental() %}

    where trade_date > (select max(trade_date) from {{ this }})

{% endif %}

group by 1, 2