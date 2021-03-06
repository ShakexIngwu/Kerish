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
// SmartRule struct for SmartRule
type SmartRule struct {
	Active string `json:"active,omitempty"`
	AlertRuleKey string `json:"alertRuleKey,omitempty"`
	Field string `json:"field,omitempty"`
	Remark string `json:"remark,omitempty"`
	// Example: 'earnPre', 'fastUp', 'fastDown', 'week52Up', 'week52Down', 'day5Down'
	Type string `json:"type,omitempty"`
}
