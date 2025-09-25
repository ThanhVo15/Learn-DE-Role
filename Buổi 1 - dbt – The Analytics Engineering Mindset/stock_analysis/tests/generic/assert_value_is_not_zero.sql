{% test assert_value_is_not_zero(model, column_name) %}
    select *
    from {{ model }}
    where {{ column_name }} = 0
{% endtest %}