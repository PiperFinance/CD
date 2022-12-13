package schema

import (
	"github.com/ethereum/go-ethereum/common"
	"math/big"
)

type ChainToken struct {
	ChainId `json:"chainId"`
	Tokens  []Token `json:"tokens"`
}

type TokenBalanceResponse struct {
	Tokens     []Token   `json:"tokens"`
	Networks   []ChainId `json:"networks"`
	Symbol     `json:"symbol"`
	Name       `json:"name"`
	Price      `json:"price"`
	ValueSum   big.Float `json:"valueSum"`
	BalanceSum big.Float `json:"balanceSum"`
}

type ArrayOfAddress struct {
	Addresses []common.Address
}

/////////////////////////////////////////

func (t Wallet) Get() common.Address {
	return t.Address
}
