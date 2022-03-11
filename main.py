import asyncio, aiohttp, aiofiles
from json_database import JsonStorage
from typing import Optional
from fastapi import FastAPI, Header, Request, Response, status
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
databasePath = "database.db"
db = JsonStorage(databasePath, True)
apiKey = "82dd2e07d8fb8aed10789c9135cd742566dffcd6"
headers = {"Authorization": f"Bearer {apiKey}"}


def checkHWID(hwid, ip):
    s = list(set(db[hwid]["ip"]))
    s.append(ip)
    db[hwid]["ip"] = list(set(s))
    db.store()
    if hwid in db["hwids"]:
        return True
    return False


async def returnFilterServers(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://backend.mcstalker.com/api/filterservers",
            data=payload,
            headers=headers,
        ) as resp:
            return await resp.json()


async def returnVersions():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://backend.mcstalker.com/api/versions", headers=headers
        ) as resp:
            return await resp.json()


class filterServersClass(BaseModel):
    sortMode: str
    ascdesc: str
    version: int
    country: str
    mustHavePeople: bool
    vanillaOnly: bool
    searchText: str
    page: int
    whiteListStatus: int
    authStatus: int


@app.post("/api/filterservers")
@limiter.limit("2/second")
async def getServers(
    payload: filterServersClass,
    request: Request,
    hwid: Optional[str] = Header("hwid"),
):
    if not checkHWID(hwid, request.client.host):
        return {"error": "Invalid HWID"}
    return await returnFilterServers(payload.dict())


@app.get("/api/versions")
@limiter.limit("2/second")
async def getVersions(request: Request, hwid: Optional[str] = Header("hwid")):
    if not checkHWID(hwid, request.client.host):
        return {"error": "Invalid HWID"}
    return await returnVersions()


@app.get("/mod/addHwid")
async def addHwid(
    request: Request,
    hwid: Optional[str] = Header("hwid"),
    authorisation: Optional[str] = Header("authorisation"),
    owner: Optional[str] = Header("owner"),
):
    if authorisation != "mcStalkerBased":
        return {"error": "Invalid HWID"}
    db["hwids"].append(hwid)
    db[hwid] = {"id": owner, "ip": []}
    db.store()


@app.get("/mod/checkHwid")
@limiter.limit("1/minute")
async def checkHwid(
    hwid: Optional[str] = Header("hwid"),
    request: Request = Request,
    response: Response = Response,
):
    if hwid in db["hwids"]:
        response.status_code = status.HTTP_200_OK
        return True
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return False


@app.get("/mod/checkHwidAuth")
async def checkHwid(
    hwid: Optional[str] = Header("hwid"),
    authorisation: Optional[str] = Header("Authorisation"),
    response: Response = Response,
):
    if authorisation != "mcStalkerBased":
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "Invalid Authorisation"}
    if hwid in db["hwids"]:
        response.status_code = status.HTTP_200_OK
        return True
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return False


@app.get("/mod/returnIllegitimateHwids")
async def returnBadHwids(authorisation: Optional[str] = Header("Authorisation")):
    if authorisation != "mcStalkerBased":
        return {"error": "Invalid HWID"}
    ill = []
    for hwid in db.keys():
        if hwid not in db["hwids"]:
            ill.append({hwid: db[hwid]})
    ill.remove({"hwids": db["hwids"]})
    return ill


@app.get("/mod/returnAllHwids")
async def returnLegalHwids(authorisation: Optional[str] = Header("Authorisation")):
    if authorisation != "mcStalkerBased":
        return {"error": "Invalid HWID"}
    hwids = {"list": []}
    for hwid in db["hwids"]:
        hwids["list"].append(hwid)
    for hwid in hwids["list"]:
        hwids[hwid] = db[hwid]
    return hwids


@app.get("/mod/revokeHWID")
async def revokeHwid(
    hwid: Optional[str] = Header("hwid"),
    authorisation: Optional[str] = Header("Authorisation"),
):
    if authorisation != "mcStalkerBased":
        return {"error": "Invalid HWID"}
    if hwid in db["hwids"]:
        db["hwids"].remove(hwid)
        db.store()
        return True
    return False


verDb = JsonStorage("versionDatabase.db")


@app.get("/mod/changeVersion")
async def changeVersion(
    authorisation: Optional[str] = Header("Authorisation"),
    version: Optional[str] = Header("Version"),
    url: Optional[str] = Header("downloadUrl"),
    authorisedBy: Optional[str] = Header("authorisedBy"),
):
    if authorisation != "mcStalkerBased":
        return {"error": "Invalid HWID"}
    verDb["version"] = {
        "versionString": version,
        "downloadUrl": url,
        "authorisedBy": authorisedBy,
    }
    verDb.store()
    return True


@app.get("/mod/showVersion")
async def showVersion():
    return verDb["version"]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
