drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  text string not null,
  author string not null,
  category string not null
);
