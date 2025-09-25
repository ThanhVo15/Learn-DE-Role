-- Một bài test trong dbt thành công nếu nó trả về 0 dòng.
-- Do đó, chúng ta cần viết một câu lệnh SELECT để tìm ra các dòng "xấu".

select 
    trade_id,
    volume
from 
    {{ ref('stg_trades')}}
where
    volume <= 0