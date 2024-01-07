import requests
import json
import datetime
import random
import os
import time

RPC_USER = 'nanocheeze'
RPC_PASSWORD = 'ncz'
RPC_HOST = '192.168.1.1'
RPC_PORT = '12782'


def generate_filename(block_number, prefix="raw"):
    today = datetime.date.today()
    # Use os.path.join for proper path handling on Windows
    return os.path.join("logs", f"{prefix}_{today.isoformat()}.txt")


def call_rpc(method, params=[], filename=""):
    if filename:
        with open(filename, 'a') as file:
            url = f'http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}'
            headers = {'content-type': 'application/json'}
            payload = json.dumps({"jsonrpc": "1.0", "id": "curltest", "method": method, "params": params})
            file.write(f"Calling RPC method: {method} with params: {params}\n")
            try:
                response = requests.post(url, headers=headers, data=payload)
                response.raise_for_status()
                result = response.json().get('result')
                file.write(f"RPC Response for {method}: {result}\n")
                return result
            except requests.exceptions.HTTPError as http_err:
                file.write(f"HTTP error occurred: {http_err}\n")
                file.write("Response content: {}\n".format(response.content))
                if "Block number out of range" in response.text:
                    return "error_block_out_of_range"
            except Exception as e:
                file.write(f"An error occurred: {e}\n")
            return None
    else:
        # Handle the call without writing to a file
        url = f'http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}'
        headers = {'content-type': 'application/json'}
        payload = json.dumps({"jsonrpc": "1.0", "id": "curltest", "method": method, "params": params})
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json().get('result')
        except Exception:
            return None

def get_block_transactions(block_number, filename=""):
    block_hash = call_rpc('getblockhash', [block_number], filename)
    if block_hash == "error_block_out_of_range":
        return [], True
    if not block_hash:
        return [], False

    block_info = call_rpc('getblock', [block_hash], filename)
    if not block_info:
        return [], False

    return block_info.get('tx', []), False

def get_op_return_data(block_number, txid, filename=""):
    raw_tx = call_rpc('getrawtransaction', [txid, 1], filename)
    if not raw_tx:
        return None

    for vout in raw_tx.get('vout', []):
        if 'scriptPubKey' in vout and 'asm' in vout['scriptPubKey']:
            asm = vout['scriptPubKey']['asm']
            if asm.startswith('OP_RETURN'):
                hex_data = asm.split(' ')[1]
                counter=True
                while len(hex_data) > 0:
                    
                    try:
                        # Attempt to decode the hex data
                        decoded_data = bytes.fromhex(hex_data).decode('utf-8')
                        if counter:
                            decoded_data = bytes.fromhex(hex_data).decode('utf-8')[2:]
                        return block_number, txid, hex_data, decoded_data
                    except UnicodeDecodeError:
                        counter=False
                        # Remove the first two characters and retry
                        hex_data = hex_data[2:]
                    except Exception as e:
                        print(f"Error decoding OP_RETURN data: {e}")
                        break
                print(f"Unable to decode OP_RETURN data for txid {txid}")
    return None



def process_block(block_number):
    raw_filename = generate_filename(block_number)
    final_filename = generate_filename(block_number, prefix="final")
    
    txids, out_of_range = get_block_transactions(block_number, raw_filename)
    if out_of_range:
        return False

    op_return_info = []
    for txid in txids:
        result = get_op_return_data(block_number, txid, raw_filename)
        if result:
            op_return_info.append(result)

    if not op_return_info:
        #print(f"No OP_RETURN data found in block {block_number}.")
        return True  # No OP_RETURNs found, so skip file saving

    final_output = f"\nDecoded OP_RETURN Data for Block {block_number}:\n"
    for info in op_return_info:
        block, txid, hex_data, decoded_data = info
        final_output += f"Block: {block}, TXID: {txid}\nHex: {hex_data}\nString: {decoded_data}\n\n"

    print(final_output)

    with open(final_filename, 'a') as file:
        file.write(final_output)

    return True

def main():
    block_number = 1544566  # Starting block number
    while True:
        success = process_block(block_number)
        if not success:
            print(f"Block number {block_number} out of range, waiting for 1 minute...")
            time.sleep(60)  # Wait for 1 minute before retrying
            continue
        block_number += 1  # Increment the block number for the next iteration

if __name__ == "__main__":
    main()
