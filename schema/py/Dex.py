from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Pair(BaseModel):
    A: int
    lp_fee: int
    address: str
    N_COINS: int
    reserves: List[int]
    decimals: List[int]
    dex: str
    type: int
    tokens: List[str]
    rates: List[str]


class Field250Item(BaseModel):
    name: str
    factory: str
    router: Optional[str] = None
    lp_fee: Optional[int] = None
    index: int
    type: int
    pairs: Optional[List[Pair]] = None


class Field4002Item(BaseModel):
    name: str
    router: str
    factory: str
    lp_fee: int
    index: int
    type: int


class Pair1(BaseModel):
    A: int
    lp_fee: int
    address: str
    N_COINS: int
    reserves: List[int]
    dex: str
    type: int
    tokens: List[str]
    rates: List[int]


class Factories(BaseModel):
    DSPFactory: str
    DVMFactory: str
    DPPFactory: str
    UpCrowdPoolingFactory: str
    CrowdPoolingFactory: str


class Field56Item(BaseModel):
    name: str
    factory: str
    router: Optional[str] = None
    index: int
    type: int
    lp_fee: Optional[int] = None
    MasterChef: Optional[str] = None
    SingleAsset: Optional[str] = None
    UTILS: Optional[str] = None
    pairs: Optional[List[Pair1]] = None
    lp_token: Optional[str] = None
    factories: Optional[Factories] = None


class Field1Item(BaseModel):
    name: str
    factory: str
    router: str
    lp_fee: int
    index: int
    type: int


class DEX(BaseModel):
    field_250: List[Field250Item] = Field(..., alias='250')
    field_4002: List[Field4002Item] = Field(..., alias='4002')
    field_56: List[Field56Item] = Field(..., alias='56')
    field_1: List[Field1Item] = Field(..., alias='1')
