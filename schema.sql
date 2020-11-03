CREATE TABLE
IF NOT EXISTS zt_guild
(
    "id" BIGINT PRIMARY KEY,
    "prefix" VARCHAR(512),
    "disabled" BIGINT[] DEFAULT '{}'
);

CREATE TABLE 
IF NOT EXISTS zt_user
(
    "id" BIGINT,
    "guild" BIGINT,
    "other_characters" BIGINT[] DEFAULT '{}',
    "main_characters" VARCHAR,
    "mc_level" BIGINT,
    "mc_xp" BIGINT   
)