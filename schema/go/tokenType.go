package schema

type TokenId string

type TokenDet struct {
	ChainId     int         `json:"chainId"`
	Address     string      `json:"address"`
	Name        string      `json:"name"`
	Symbol      string      `json:"symbol"`
	Decimals    int         `json:"decimals"`
	Tags        []string    `json:"tags"`
	CoingeckoId string      `json:"coingeckoId"`
	LifiId      interface{} `json:"lifiId"`
	ListedIn    []string    `json:"listedIn"`
	LogoURI     string      `json:"logoURI"`
	Verify      bool        `json:"verify"`
}

type Token struct {
	Token    TokenDet    `json:"token"`
	PriceUSD interface{} `json:"priceUSD"`
	Balance  string      `json:"balance"`
	Value    string      `json:"value"`
}

type TokenMapping map[TokenId]Token
