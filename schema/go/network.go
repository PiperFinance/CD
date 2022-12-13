package schema

import (
	"github.com/ethereum/go-ethereum/common"
	"net/url"
)

type Network struct {
	NativeCurrency struct {
		Name     string `json:"name"`
		Symbol   string `json:"symbol"`
		Decimals int    `json:"decimals"`
	} `json:"nativeCurrency"`
	ChainId int    `json:"id"`
	Name    string `json:"name"`
	Network string `json:"network"`
	RpcUrls struct {
		Infura  string `json:"infura"`
		Default string `json:"default"`
		Public  string `json:"public"`
	} `json:"rpcUrls"`
	Ens struct {
		Address string `json:"address"`
	} `json:"ens"`
	Multicall struct {
		Address      string `json:"address"`
		BlockCreated int    `json:"blockCreated"`
	} `json:"multicall"`
	BlockExplorers struct {
		Default struct {
			Name string `json:"name"`
			Url  string `json:"url"`
		} `json:"default"`
		Public struct {
			Name string `json:"name"`
			Url  string `json:"url"`
		} `json:"public"`
	} `json:"blockExplorers"`
	Testnet bool `json:"testnet"`
}

type NativeNetworkCurrency struct {
	Name     `json:"name"`
	Symbol   `json:"symbol"`
	Decimals `json:"decimals"`
}
type NetworkExplorer struct {
	Name     `json:"name"`
	Url      url.URL                 `json:"url"`
	Standard NetworkExplorerStandard `json:"standard"`
}
type ENS struct {
	Registry common.Address `json:"registry"`
}
