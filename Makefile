include .envvars
export
deploy:
	@echo "Deploying package to remote server $(REMOTE_SERVER)..."
	@echo "Packaging binance-bot-websocket module to binance-bot-websocket.pyz"
	@python -m zipapp binance-bot-websocket -m "app:main"
	@echo "Transferring binance-bot-websocket.pyz onto remote server $(REMOTE_SERVER)"
	@scp -i ~/.ssh/binance-bot-websocket-vm.key binance-bot-websocket.pyz $(REMOTE_SERVER):binance-bot-websocket/binance-bot-websocket.pyz