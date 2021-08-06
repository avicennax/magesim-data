from typing import Any, Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class WCLClient:
    def __init__(self, token: str):
        transport = AIOHTTPTransport(
            url='https://classic.warcraftlogs.com/api/v2/client', 
            headers={'Authorization': 'Bearer ' + token}, 
            timeout=120
        )
        
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    async def query(self, query: str, params: Dict[str, Any]):
        gql_request = gql(query)
        return await self.client.execute_async(gql_request, params)
