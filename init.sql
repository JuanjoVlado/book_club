CREATE USER bookclubms WITH PASSWORD 'bookclubms' CREATEDB;
GRANT ALL ON SCHEMA public TO bookclubms;
ALTER SCHEMA public OWNER TO bookclubms;
