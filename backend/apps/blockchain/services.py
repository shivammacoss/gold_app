import logging

from apps.wallets.models import Wallet

from .ethereum import EthereumService
from .tron import TronService

logger = logging.getLogger("blockchain")


class BlockchainServiceFactory:
    """Factory to get the correct blockchain service based on network."""

    @staticmethod
    def get_service(network: str):
        if network == Wallet.Network.TRC20:
            return TronService()
        elif network == Wallet.Network.ERC20:
            return EthereumService(network="ETH")
        elif network == Wallet.Network.BEP20:
            return EthereumService(network="BSC")
        else:
            raise ValueError(f"Unsupported network: {network}")

    @staticmethod
    def generate_wallet_address(network: str):
        """Generate a new blockchain address for the given network."""
        service = BlockchainServiceFactory.get_service(network)
        return service.generate_address()

    @staticmethod
    def send_usdt(network: str, to_address: str, amount: float):
        """Send USDT on the given network."""
        service = BlockchainServiceFactory.get_service(network)
        return service.send_usdt(to_address, amount)
