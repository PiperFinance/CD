import logging
import requests
import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel

import schema

logger = logging.getLogger(__name__)


# @dataclass(init=True)
class Providers(BaseModel):
    name: str
    timestamp: str | datetime
    version: Optional[dict]
    keywords: dict
    tags: dict
    logoURI: str
    tokens: List[schema.Token]

    @classmethod
    def load(cls, url, name=None, provider_dir=None):
        if provider_dir is None:
            provider_dir = os.getenv('PROVIDER_DIR', 'provider')
        r = requests.get(url)

        if r.status_code == 200:
            try:
                res = r.json()
                if name is None:
                    name = res.get('name')
                    assert name, "No Value Found for name"
                if "tokens" in res.keys():
                    tokens = [schema.Token(**token) for token in res['tokens']]
                    provider = Providers(
                        name=name,
                        timestamp=datetime.now().isoformat()+"Z",
                        version=res.get("version", {}),
                        keywords=res.get("keywords", {}),
                        tags=res.get("tags", {}),
                        logoURI=res.get("logoURI", {}),
                        tokens=tokens
                    )
                    with open(os.path.join(provider_dir, name + ".json"), "w+") as f:
                        json.dump(provider.json(), f)
            except json.JSONDecodeError:
                logger.error(f"Bad Request @ {name} :  { r.text}")
