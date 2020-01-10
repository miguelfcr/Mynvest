create DATABASE mynvest;

\c mynvest;

CREATE USER mynvest WITH PASSWORD 'mynvest';
grant all privileges on database mynvest to mynvest;