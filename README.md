NanoCheeZe Virtual Crypto Tokens

1/11/2024
made a small update to main.cpp to account for the chain enforcement protocol now that op_returns are available. nodes running in txindex mode were unable to move past any blocks with 0 burn op_returns. I added this code somewhere around line 780 in main.cpp and it works like butter.

BOOST_FOREACH(const CTxOut& txout, vout){   if (!txout.IsEmpty())   {       // Check if the first opcode is OP_RETURN
        if (txout.scriptPubKey.size() > 0 && txout.scriptPubKey[0] == OP_RETURN) {
            // This is an OP_RETURN output, so it's unspendable and can bypass the check
            continue;        }
        if (txout.nValue < MIN_TXOUT_AMOUNT) { return DoS(100, error("CTransaction::CheckTransaction() : txout.nValue below minimum")); }  }}

OP_RETURNS have been implemented into NCZ crypto tokens! 255 character limi.
Python script are available in the main repo directory to send and get messages with OP_RETURN commands.

If you are having trouble with connecting to the RPC server, try launching "./NanoCheeZe-qt -txindex -daemon"

easy compile instructions for ubuntu 12 and 14

Step 1:

wget "https://raw.githubusercontent.com/cybershrapnel/NanoCheeZe/master/build_ncz"

Step 2:

on ubuntu 16 and below just type the following command in a terminal after doing step 1.

command to use:

bash build_ncz

See the readme for other install options and the windows exe of the NanoCheeZe-qt app!

1/9/2024
FInally got OP_RETURN commands implemented and working right. Updated version numbers. Update your client or you will fork. The old V2 client will not allow new block rules. Changes may still be needed, so please keep up to date.

Ordinal Inscriptions next. Still working out the proof of reclamation thing.

5/20/21
updated staking rewards limits to reduce by 50% every 1 million blocks starting at 1 million.
Lessons learned from Hobonickels is that MAX_MONEY is not the supply limit of coins but the tx transfer limit.
There is no cap on coin production, but after 8 million blocks coin reward reduction for staking should effectively cap the market where it is at that time.
Update your clients or get forked at block 1 million.

4/21/2021
ok, found a bug, silly stupid mistake... client was trying to open node on 12782 port, but config file is force setting 12781, and then the rpc port jumps in there and starts arguing with the node discovery protocol.... So basically clients have been trying to connect on the rpc port.... Everyone is gonna need to update to this new build I pushed to github.... Will compile a new windows build soon (in progress) This will resolve no connection issues.

6/26/2020
Fixed compiling for Ubuntu 18 and up. simple OpenSSL version issue. pretty mad now that I found the problem lol... Still haven't investigated the boost issue with what I mentioned in the last update, but I suspect this may resolve it? I haven't tried yet though... but it compiles on ubuntu 18 for sure now. Haven't tested anything else but I think 19 and 20 will work too? will update later.

Note/Update: (1/10/2020)
I have commented out lines 212-216 in the rpcrawtransaction.cpp file. The boost libraries are halting compiling on Ubuntu 16+ running certain ecosystems.  I will investigate this further. The nanocheezed and qt apps work just fine but obviously commenting out that section will effect the rawtransaction command using boost. I don't think this will be an issue though

* Staking:
  * 100% Max Yearly Stake Reward
  * 20% Min Stake Reward
  * 250 Max Reward Cap (reduced 50% every 1 million blocks)
  * 13 day min weight, 30 days max weight.
  
* Based on NVC/BitGems/Bottlecaps/Hobonickels
* Proof of Work/Proof of Stake Hybrid. 
* Developing Proof of Reclamation
* Scrypt
* Linear Difficulty Retarget
* 25 Confirms
* 5 Tokens Per Block
* No True Coin Limit
* Default P2P Port: 12781
* Default RPC Port: 12782
* Dynamically Loadable Wallets 
* Updated Coin Control
* Easy Accessible Peer, Stake, and Block information
* Stake Splitting
* Built in Block Browser and Network Graph
* Configurable splitthreshold and combinethreshold
* 1 minute wait time for PoW blocks following a PoW block.
* ~2 minute retarget time (should see block times of 30 seconds to 3 minutes)
