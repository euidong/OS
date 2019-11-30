# Implementation Contiguous Allocation

### requirement
- Allocation
  - 자원 할당이 효율적으로 수행된다.
  - 가장 적절한 위치에 자원이 할당된다. (최대한 빈 공간의 수를 줄이는 방향으로)
- Deallocation
  - 해제 시에는 해당 자원을 성공적으로 돌려준다.
  - coalsing 처리
    - 만약, 빈공간이 연속으로 발생하면 해당 빈공간끼리는 구분을 없애고 합쳐준다.
- compaction
  - 효율적인 compaction을 위해 빈 공간과 이동해야 하는 할당 공간의 크기가 같다면 해당 할당 공간을 그곳으로 배치.
  - 그게 불가능하다면, 모든 빈공간을 모은다.

### input
- 유인물과 동일한 형태(.txt file)

### output
- 1. 유인물과 동일한 형태(output form)
- 2. plotly를 이용한 bar graph.
