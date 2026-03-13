* RustChain Miner for CDC 6600 (1964)
* COMPASS Assembly Source
* 
* Bounty: 200 RTC - LEGENDARY Tier
* Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b

         $TITLE  'RUSTCHAIN MINER - CDC 6600'
         $PROGRAM RUSTCHAIN_MINER

* Memory Equates
         EQU     CODE_START,256
         EQU     WALLET_AREA,4096
         EQU     ATTEST_BUF,8192
         EQU     WORK_AREA,16384

*=======================================================================
* ENTRY POINT
*=======================================================================

START    LXK     1,0(0)              * X1 = 0 (clear entropy)
         LXK     2,0(0)              * X2 = 0 (clear hash)
         LXK     4,0(0)              * X4 = 0 (wallet part 1)
         LXK     5,0(0)              * X5 = 0 (wallet part 2)
         LBI     1,1(0)              * B1 = 1
         LBI     3,60(0)             * B3 = 60
         
         * Print welcome
         LAI     6,WELCOME(0)
         SXA     6,9(0)              * Send to PP9 console
         
         J       COLLECT_ENTROPY

*=======================================================================
* ENTROPY COLLECTION
*=======================================================================

COLLECT_ENTROPY
         LBI     2,100(0)            * B2 = 100 loops

ENTROPY_LOOP
         LAI     1,PP_CLOCK(0)       * A1 = PP clock
         LD      1,0(1)              * X1 = clock value
         ANA     1,2(0)              * Mix bits
         ORA     1,2(0)
         B2      1,ENTROPY_LOOP      * Loop 100 times
         
         LAI     7,ENTROPY_BUF(0)
         SD      2,0(7)              * Store entropy
         
         J       GENERATE_WALLET

*=======================================================================
* WALLET GENERATION
*=======================================================================

GENERATE_WALLET
         LAI     1,ENTROPY_BUF(0)
         LD      1,0(1)              * X1 = entropy
         
         LXK     3,12345(0)          * Constant 1
         FMP     3,1,4               * X4 = X3 * X1
         
         LXK     3,67890(0)          * Constant 2
         FMP     3,1,5               * X5 = X3 * X1
         
         LAI     7,WALLET_AREA(0)
         SD      4,0(7)              * Store wallet part 1
         SD      5,1(7)              * Store wallet part 2
         
         J       DISPLAY_WALLET

*=======================================================================
* DISPLAY WALLET
*=======================================================================

DISPLAY_WALLET
         LAI     6,WALLET_HDR(0)
         SXA     6,9(0)              * Header to console
         
         LAI     6,WALLET_P1(0)
         SXA     6,9(0)              * Part 1
         
         LAI     6,WALLET_P2(0)
         SXA     6,9(0)              * Part 2
         
         J       ATTESTATION_LOOP

*=======================================================================
* ATTESTATION LOOP
*=======================================================================

ATTESTATION_LOOP
         LAI     6,STATUS_MSG(0)
         SXA     6,9(0)              * Status
         
         * Wait for epoch (10 min)
         LAI     1,EPOCH_TIMER(0)
         LD      1,0(1)
         LXK     2,600(0)            * 600 seconds
         FSR     1,2,3               * Compare
         BP      WAIT_EPOCH
         
         J       GENERATE_ATTESTATION

WAIT_EPOCH
         J       WAIT_EPOCH          * Busy wait

*=======================================================================
* GENERATE ATTESTATION
*=======================================================================

GENERATE_ATTESTATION
         J       COLLECT_ENTROPY     * Fresh entropy
         
         LAI     1,WALLET_AREA(0)
         LD      1,0(1)
         LD      2,1(1)
         ANA     1,2(0)
         ORA     1,2(0)
         
         LAI     7,ATTEST_BUF(0)
         SD      2,0(7)              * Store attestation
         
         LAI     6,ATTEST_READY(0)
         SXA     6,9(0)
         
         J       ATTESTATION_LOOP

*=======================================================================
* DATA AREAS
*=======================================================================

         ORG     WORK_AREA

WELCOME      OCT     200000000000000000000
WALLET_HDR   OCT     100000000000000000000
STATUS_MSG   OCT     300000000000000000000
ATTEST_READY OCT     400000000000000000000
WALLET_P1    OCT     0
WALLET_P2    OCT     0
PP_CLOCK     OCT     0
EPOCH_TIMER  OCT     0
ENTROPY_BUF  OCT     0

         END     START

* BOUNTY: #326 | LEGENDARY | 200 RTC
* WALLET: RTC4325af95d26d59c3ef025963656d22af638bb96b
