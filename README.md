Made this public to show an acquaintance how to make an actually good HWID Authentication API (they used pastebin auth before, wtf).

- `main.py` - The actual API, has checking for versioning, HWIDs, and more. Since it was originally made as a proxy for the MCStalker API, it has some routes regarding it. Access the docs by running the API and going to `localhost:8000/redoc`.

- `bot.py` - The discord bot interface for the API. Prefix is `h!` or `!!`.

----

The point of this program was to act as a proxy for the MCStalker Mod, during the period where it was 8 invites/level 40/boost to access. To enforce this, we had to add HWID Authentication to the mod, since the mod's server browser relied on the MCStalker API to display servers, we added HWID Authentication to an API Proxy, all the requests from the mod were passed through this proxy, the HWID was checked, and then it was passed on to the MCStalker API, and the response from the MCStalker API was parsed and returned to the mod.

The databases (`database.db`, `versionDatabase.db`) are JSON because we wanted to make it easy to modify, else I would've used `aiosqlite`. If I were to recode it now, the one feature I would probably add is routes, it would make the codebase cleaner and make prefixing (`/mod/`, `/api/`, etc) routes easier.

Anyway, the intended use-case of this application was to act as a proxy between a client-side application and the server API, the proxy authenticated requests and relayed them to the server, if they were valid.

MCStalker was created by [SSouper](https://github.com/SSouper), and [Simulatan](https://github.com/SIMULATAN) developed the 1.17 Fabric Mod, you can view a full list of credits [here](https://github.com/MC-Stalker/Credits-and-Acknowledgments/blob/main/README.md). This proxy was developed by [TheOnlyWayUp](https://github.com/TheOnlyWayUp).

---

Using

```cmd
python3.9 -m pip install discord jishaku fastapi slowapi aiofiles json_database

cd source && python3.9 main.py
```

^^ After git cloning the repo.