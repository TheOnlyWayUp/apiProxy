At the time of writing, `database.db`'s current contents are -
```json
{
    "hwids": [
        "basedTesting"
    ],
    "basedTesting": {
        "id": "876055467678375998",
        "ip": [
            "206.189.205.251",
            "2"
        ]
    },
    "epic": {
        "id": "505713760124665867",
        "ip": []
    }
}
```
`hwids` is a list of authorised HWIDs, all other keys are HWIDs, who they're for and what IPs accessed them.

For example, if your HWID is 123, the database would look like
```json
{
    "hwids": [
        "123"
    ],
    "123": {
        "id": "your discord id",
        "ip": [
            "your ip address"
        ]
    }
}
```
Unauthorized HWIDs are also logged, if an HWID is unauthorized, it will be present as a key in the database but not a part of the `hwids` array. The bot has commands to show unauthorized HWIDs, beware though, revoked HWIDs will show up as unauthorized.