create table if not exists movie
(
	"movieID" bigserial not null primary key,
	"title" varchar(120) not null,
	"watches" bigint not null
);

create table if not exists movielist
(
	"movielistID" bigserial not null primary key,
	"title" varchar(120) not null,
	"url" varchar(120) not null
);

create table if not exists movie_movielist
(
	"moviemovielistID" bigserial not null primary key,
	"movieID" integer not null references movie("movieID") on update cascade on delete cascade,
	"movielistID" integer not null references movielist("movielistID") on update cascade on delete cascade
);


Insert INTO movie ("title", "watches") VALUES ('Freaky', 345286);
Insert INTO movie ("title", "watches") VALUES ('The Adventures of Sharkboy and Lavagirl in 3-D', 135325);
Insert INTO movie ("title", "watches") VALUES ('Cats', 532535);
Insert INTO movie ("title", "watches") VALUES ('The Emoji Movie', 835325);


Insert INTO movielist ("title", "url") VALUES ('Letterboxds 1,000 Most Watched Films', 'https://letterboxd.com/ur_mom_lol/list/letterboxds-1000-most-watched-films/');

Insert INTO movie_movielist ("movieID", "movielistID") VALUES (1, 1);
Insert INTO movie_movielist ("movieID", "movielistID") VALUES (2, 1);
Insert INTO movie_movielist ("movieID", "movielistID") VALUES (3, 1);
Insert INTO movie_movielist ("movieID", "movielistID") VALUES (4, 1);
