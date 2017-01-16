create schema weibo;
use weibo;

create table tweet_users (
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

create table sina_users (
	Sid varchar(32),
	Pwd varchar(32),
	Avaiable boolean,
	Reason varchar(512)
);

create table sys_logs (
	Lid int primary key auto_increment,
	ProcessID bigint,
	LogTime varchar(20),  /*2017-01-01 00:00:00*/
	UserCount int,
	TweetCount int,
	MsgType varchar(32),
	Message varchar(1024)
);

create table sys_params (
	Pid int primary key auto_increment,
	ParamCode varchar(32),
	ParamName varchar(32),
	ParamValue varchar(32),
	Enabled boolean not null default true
);
insert into sys_params (pid, paramcode, paramname, paramvalue) values (1, 'isRun', '运行状态', 0);

create table sys_users (
	Suid varchar(32) not null,
	Suname varchar(32) not null,
	Pwd varchar(32)
);
insert into sys_users (suid, suname, pwd) values ('Admin', '系统管理员', '123456');