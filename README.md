NanoCheeZe Virtual Crypto Tokens
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
