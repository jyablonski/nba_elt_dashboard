-- Latest season's payroll position relative to the cap and apron thresholds.
select
    team,
    season,
    total_payroll,
    total_market_value,
    total_surplus,
    roster_count,
    salary_cap,
    luxury_tax_threshold,
    pct_of_cap,
    is_above_cap,
    is_above_luxury_tax,
    is_above_first_apron,
    is_above_second_apron
from team_payroll_summary
where team = :abbreviation
order by
    season desc
limit 1
