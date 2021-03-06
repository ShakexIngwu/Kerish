/*
 * Webull API
 *
 * Webull API Documentation
 *
 * API version: 3.0.1
 * Contact: austin.millan@gmail.com
 * Generated by: OpenAPI Generator (https://openapi-generator.tech)
 */

package openapi
// PaperOrder struct for PaperOrder
type PaperOrder struct {
	Action OrderSide `json:"action,omitempty"`
	CanCancel bool `json:"canCancel,omitempty"`
	CanModify bool `json:"canModify,omitempty"`
	CreateTime string `json:"createTime,omitempty"`
	CreateTime0 int64 `json:"createTime0,omitempty"`
	FilledQuantity string `json:"filledQuantity,omitempty"`
	LmtPrice string `json:"lmtPrice,omitempty"`
	OrderId int32 `json:"orderId,omitempty"`
	OrderType OrderType `json:"orderType,omitempty"`
	OutsideRegularTradingHour bool `json:"outsideRegularTradingHour,omitempty"`
	PaperId int32 `json:"paperId,omitempty"`
	PlacedTime string `json:"placedTime,omitempty"`
	Status string `json:"status,omitempty"`
	StatusStr string `json:"statusStr,omitempty"`
	Ticker GetOrdersItemTicker `json:"ticker,omitempty"`
	TimeInForce TimeInForce `json:"timeInForce,omitempty"`
	TotalQuantity string `json:"totalQuantity,omitempty"`
}
