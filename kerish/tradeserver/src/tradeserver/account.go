package tradeserver

import (
	"encoding/json"
	"github.com/kerish/webull-client/webull"
	model "github.com/kerish/webull-openapi/openapi"
	"io/ioutil"
	"os"
)

const AccInfoJsonFile = "/opt/kerish/acc_info.json"

type AccountInfo struct {
	Username   string `json:"username"`
	Password   string `json:"password"`
	DeviceName string `json:"device_name"`
	TradePIN   string `json:"trade_pin"`
	MFA        string `json:"mfa"`
}

type Order struct {
	OrderID string
	Action model.OrderSide

}

type Account struct {
	client *webull.Client
	orders
}

var Accounts = make(map[string]Account)

func NewAccounts() error {
	accountInfoMap := make(map[string]AccountInfo)
	jsonFile, err := os.Open(AccInfoJsonFile)
	if err != nil {
		return err
	}
	byteValue, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		return err
	}

	err = json.Unmarshal(byteValue, &accountInfoMap)
	if err != nil {
		return err
	}

	for accKey, accInfo := range accountInfoMap {
		cred := &webull.Credentials{
			Username:    accInfo.Username,
			Password:    accInfo.Password,
			TradePIN:    accInfo.TradePIN,
			MFA:         accInfo.MFA,
			DeviceName:  accInfo.DeviceName,
			AccountType: model.AccountType(2), // 1: phone number, 2: email
		}
		client, err := webull.NewClient(cred)
		if err != nil {
			return err
		}

		err = client.TradeLogin(*cred)
		if err != nil {
			return err
		}

		Accounts[accKey] = Account{
			client: client,
		}
	}
	return nil
}
