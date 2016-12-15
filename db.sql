create schema weibo;
use weibo;

create table users (
    Uid varchar(32),
    Uname varchar(128),
	Verified boolean,
	VerifiedType varchar(200),
	VerifiedKind int,
	Gender varchar(2),
	GeoEnabled boolean,
	Province varchar(32),
	FollowersCount int,
	FriendsCount int,
	BiFollowersCount int,
	StatusesCount int,
	FavouritesCount int
);

create table tweets (
	Mid varchar(32),
	Text varchar(10000),
	Time varchar(32),
	Uid varchar(32),
	RegPostTime varchar(32),
	RepostCommentCount int,
	ShareCount int,
	AttributesCount int,
	Rumor boolean
);
