from web3 import Web3
from eth_account import Account

class EthereumWallet:
    def __init__(self):
        self.w3 = None
        self.account = None
        self.connected = False

    def connect_wallet(self, infura_url, wallet_address, private_key):
        try:
            self.w3 = Web3(Web3.HTTPProvider(infura_url))
            self.account = Account.from_key(private_key)
            
            # Verify that the provided address matches the private key
            if self.account.address.lower() != wallet_address.lower():
                print("Error: The provided wallet address does not match the private key.")
                return

            self.connected = self.w3.is_connected()
            if self.connected:
                print(f"Wallet connected. Address: {self.account.address}")
            else:
                print("Failed to connect to the Ethereum network.")
        except Exception as e:
            print(f"Error connecting wallet: {str(e)}")

    def disconnect_wallet(self):
        if self.connected:
            self.w3 = None
            self.account = None
            self.connected = False
            print("Wallet disconnected.")
        else:
            print("No wallet is currently connected.")

    def swap_asset(self, token_address, amount):
        if not self.connected:
            print("Wallet is not connected. Please connect first.")
            return

        try:
            # This is a simplified example and doesn't perform a real swap
            # In a real scenario, you would interact with a DEX like Uniswap
            token_contract = self.w3.eth.contract(address=token_address, abi=[])  # Simplified ABI
            tx = {
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'to': token_address,
                'value': self.w3.to_wei(amount, 'ether'),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
            }
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"Swap transaction sent. Transaction hash: {tx_hash.hex()}")
        except Exception as e:
            print(f"Error during swap: {str(e)}")

def main():
    wallet = EthereumWallet()

    while True:
        print("\n1. Connect Wallet")
        print("2. Swap Asset")
        print("3. Disconnect Wallet")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            infura_url = "https://arbitrum-sepolia.infura.io/v3/daf5d0baf7da4de09b0753b39be39276" #input("Enter your Infura URL: ")
            wallet_address = "0x953B8D856ae36d35D259c33F346c5Ac3D1bA6100" #input("Enter your wallet address: ")
            private_key = "9e136c7743b95eaf914e377b8e91778d88792d7660ce9fee8b417077455007c0" #input("Enter your private key: ")
            wallet.connect_wallet(infura_url, wallet_address, private_key)
        elif choice == '2':
            if not wallet.connected:
                print("Please connect your wallet first.")
            else:
                token_address = input("Enter token address to swap: ")
                amount = float(input("Enter amount to swap: "))
                wallet.swap_asset(token_address, amount)
        elif choice == '3':
            wallet.disconnect_wallet()
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()