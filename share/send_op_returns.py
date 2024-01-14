import requests
import json
import binascii
import random

RPC_USER = 'nanocheeze'
RPC_PASSWORD = 'ncz'
RPC_HOST = '192.168.1.100'
RPC_PORT = '12782'
#set these to your local NCZ node NanoCheeZe-qt or nanocheezed
#default config should be setup but you may need to make adjustments
#Also set address at bottom of page

def call_rpc(method, params=[]):
    url = f'http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}'
    headers = {'content-type': 'application/json'}
    payload = json.dumps({"jsonrpc": "1.0", "id": "curltest", "method": method, "params": params})
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json().get('result')
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print("Response content:", response.content)
    except Exception as e:
        print(f"An error occurred: {e}")
    return None





def send_raw_transaction(signed_hex):
    try:
        if not isinstance(signed_hex, str):
            raise ValueError("signed_hex must be a string")

        payload = {
            "jsonrpc": "1.0",
            "id": "curltest",
            "method": "sendrawtransaction",
            "params": [signed_hex]  # Pass as a list containing the hex string
        }

        response = call_rpc('sendrawtransaction', [signed_hex])
        if response is None:
            print("RPC call for sendrawtransaction failed")
            return False  # Indicate failure
        else:
            print("Transaction sent successfully. TXID:", response)
            return True  # Indicate success
    except Exception as e:
        print(f"An error occurred while sending the transaction: {e}")
        return False



def create_op_return_tx(message, address):
    message_hex = binascii.hexlify(message.encode('utf-8')).decode('utf-8')
    op_return_data = message_hex
    fee = 0.001  # Starting fee
    max_fee = 0.005  # Maximum fee
    retry_attempts = 12  # Number of retries per fee increment

    while fee <= max_fee:
        for attempt in range(retry_attempts):
            unspent = call_rpc('listunspent', [0, 9999999, [address]])
            if unspent is None or not unspent:
                print("No unspent outputs for address, or RPC call failed.")
                return None
            else:
                print(f"fee: {fee} - Total unspent outputs: {len(unspent)}")

                # Select one random coinblock for the transaction
                selected_unspent = random.choice(unspent)
                print("Selected Coinblock:", selected_unspent)

                inputs = [{"txid": selected_unspent['txid'], "vout": selected_unspent['vout']}]
                change_amount = selected_unspent['amount'] - fee
                if change_amount <= 0:
                    print("Error: Fee is higher than or equal to the UTXO amount. Retrying...")
                    continue  # Retry with the same fee

                outputs = {address: change_amount, "data": op_return_data}
                raw_tx = call_rpc('createrawtransaction', [inputs, outputs])
                print(inputs)
                print(outputs)
                if not raw_tx:
                    print("RPC call for createrawtransaction failed")
                    return None

                signed_tx = call_rpc('signrawtransaction', [raw_tx])
                if not signed_tx or 'hex' not in signed_tx:
                    print("RPC call for signrawtransaction failed")
                    return None

                signed_tx_hex = signed_tx['hex']
                print(f"Total fee: {fee} - Signed Transaction:", signed_tx_hex)
                if send_raw_transaction(signed_tx_hex):
                    return  # Successful transaction
                else:
                    print("Transaction failed, retrying...")

        # Increment fee after retry_attempts
        fee += 0.001
        print(f"Increasing fee to: {fee}")

    print("Failed to send transaction after reaching max fee.")




# Prompt user for a message
while True:
    while True:
        message = input("Enter your message: ")

        if len(message) > 255:
            print("Error: Message length exceeds 255 characters. Please try again.")
            continue
        elif len(message) > 80:
            print("Warning: Message length is over 80 characters. This will result in extra bloat data being sent to the signature area of the tx and will need to be accounted for when extracting data.")
            confirm = input("Do you want to proceed? (y/n): ")
            if confirm.lower() != 'y':
                continue

        break

    #REPLACE WITH YOUR ADDRESS TO SEND CHANGE BACK TO
    address = "NNd9s9o6HS8FKpzVKdR72sZWmHv1UW239f"
    message_hex2 = binascii.hexlify(message.encode('utf-8')).decode('utf-8')
    print(message_hex2)
    print (message)
    create_op_return_tx(message, address)
