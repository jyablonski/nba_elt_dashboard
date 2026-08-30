-- Blown leads and comebacks, split by season type (regular season / playoffs).
select
    season_type,
    blown_leads_10pt,
    blown_lead_rank,
    team_comebacks_10pt,
    comeback_rank,
    net_comebacks,
    net_rank
from team_blown_leads
where team = :abbreviation
order by
    season_type
limit 5
