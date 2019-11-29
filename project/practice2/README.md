# Safety algorithm
- 해당 과제는 safety algorithm을 구현하는 것을 목표로 한다.

### requirments
- safety sequency를 시작하기 전에 random process의 request가 발생한다.(단, 이로 인해 할당이 불가능해서는 안된다.)
- 그 후로, safety sequency를 실행한다.

### input
- input은 파일을 통해 입력받는다.
    - first line : process Number (100 미만)
    - Second line : resources Number (2 이상 10 미만)
    - last line : each total resources Number
    - rest line : process Max resources Number

### output
- safety sequency.
