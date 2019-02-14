import json
from database import db_context

# Fetch the credentials
with open('../config.json') as f:
    config = json.load(f)

with db_context(config) as ctx:
    ctx.add_illegal_phrase("100233939605_g@groups.kik.com", "LMAO")
    ips = ctx.list_illegal_phrases("100233939605_g@groups.kik.com")
    print(ips)