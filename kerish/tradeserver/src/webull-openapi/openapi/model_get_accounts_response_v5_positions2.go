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
// GetAccountsResponseV5Positions2 struct for GetAccountsResponseV5Positions2
type GetAccountsResponseV5Positions2 struct {
	ComboId string `json:"comboId,omitempty"`
	ComboTickerType string `json:"comboTickerType,omitempty"`
	Positions []GetAccountsResponseV5Positions `json:"positions,omitempty"`
}
