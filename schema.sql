drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  mood integer not null,
  lat real null,
  long real null
);
