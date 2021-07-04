from quart import Quart

from singleton.client import Bert


app = Quart(__name__)


@app.route("/api/servers/list")
async def server_list():
    client = Bert.getInstance()
    servers = []

    for guild in client.guilds:
        servers.append({
                "name": guild.name,
                "id": guild.id,
                "icon": str(guild.icon_url)
            })

    return {"servers": servers}
