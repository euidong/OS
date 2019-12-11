# Buffer cache's Get Block algorithm Implementation

### Input
x

### Condition
1. hash-queue and free-list is written randomly.(0~100)
2. hash-queue's mod is between 3 and 10
3. implement free list to double-linked-list.
3. make busy block randomly and duration is also random. (but, in 10s)
4. select delay block randomly.
5. block request is random block.
6. must show 5 senario of get block.

### Output
- 5 senarios of getBlock
- this program repeat getting block untill 5 senarios is executed.
- allocation was executed every 1seconds.
- I made all free buffer to busy when all senario is done except seanrio 4 to show it.
