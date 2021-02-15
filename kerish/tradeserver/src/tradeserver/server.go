package tradeserver

import (
	"github.com/gin-gonic/gin"
)

const (
	defaultPort = 8000
	currentVersion = "api/v1"
)

type TradeServer struct {
	Port int
	Router *gin.Engine
}

func NewTradeServer() *TradeServer{
	err := NewAccounts()
	if err != nil {
		panic(err)
	}

	return &TradeServer{
		Port:   defaultPort,
		Router: gin.Default(),
	}
}

func (t *TradeServer) Work() error {

}

func (t *TradeServer) configureRoutes() error {
	v1 := t.Router.Group(currentVersion)

}

func (t *TradeServer) buildOrderRoutes(parent *gin.RouterGroup) {
	order := parent.Group("order")
	order.GET("/", t.)
}

func (t *TradeServer) pullOrders() error {

}