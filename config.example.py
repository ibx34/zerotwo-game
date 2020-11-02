## Token: discord developer portal -> applications -> your application -> bot -> copy token -> paste here
TOKEN = "abcdefg"

## Prefix: Your bot's default prefix. 
PREFIX = "abc"

## Owners: Your bot's owners: Bypasses cooldowns
OWNRES = [123456789]

## Extensions: Basically modules (cogs/)
EXTENSIONS = ['jishaku','cogs.Commands','cogs.Message', 'cogs.Error']

## Guild: Your bot's default guild. Developer logs and other logs' channels will be here
GUILD = 123456789

## Color: Your bot's main color. Used on the image embeds (Default will always be #ffb6c1)
COLOR = 0xffb6c1

## Database: How user data will be stored (Uses postgresql)
DB = {
    "host": "localhost",
    "database": "database",
    "user": "user",
    "password": "password",
}