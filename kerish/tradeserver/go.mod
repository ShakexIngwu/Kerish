module kerish/tradeserver

go 1.15

require (
	github.com/kerish/webull-client v0.0.0
	github.com/kerish/webull-openapi v0.0.0
)

replace (
	github.com/kerish/webull-client => ./webull-client
	github.com/kerish/webull-openapi => ./webull-openapi
)
