package schema

import "net/url"

type Name string
type Symbol string
type Decimals int32
type Price float64

//type Balance big.Float
type ChainId int64
type NetworkId uint64
type ChainName string
type NetworkExplorerStandard string
type RPCUrl url.URL
