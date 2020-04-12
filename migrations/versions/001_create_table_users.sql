CREATE TABLE IF NOT EXISTS users(
  id serial PRIMARY KEY,
  email varchar(128),
  password_hash varchar(256),
  role varchar(64),
  firstname varchar(128),
  lastname varchar(128),
  about_me text,
  created timestamptz default now()
)