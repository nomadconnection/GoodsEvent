# Overview
 > 아이콘 커뮤니케이션팀에서 굿즈 발송 이벤트에 사용할 스마트 컨트렉트 개발.
***
# Requirement Description
1. 운영자는 이벤트 시작/종료를 지정할 수 있다.
2. 이벤트 종료시 참여자는 이벤트에 참여할 수 없다.
3. 이벤트 종료 설정 후 시작 설정으로 변경할 수 있다.
4. 참여자는 질문에 대한 보기 중 한가지를 선택하고 번호만 메세지를 보내고 이벤트에 참여한다.
5. 이벤트에 중복 참여할 수 있으나 당첨시 중복 대상이 될 수 없다.
6. 중복 참여시 답변이 최신으로 갱신 된다.
7. 이벤트 당첨은 한명씩 추첨한다.
***
# Development Environment
- OS : ubuntu 18.04 (Docker = Ubuntu 18.04.1 LTS)
- python : 3.6.6
- T-bears : v1.0.6.1 (Docker)
***
# Methods
```
def owner_check(self) -> None:
```
- SCORE 실행 권한 확인.

```
@external
def event_start(self) -> None:
```
- GoodsEvent SCORE를 open 함. 소유자만 변경 가능.

```
@external
def event_stop(self) -> None:
```
- GoodsEvent SCORE를 close 함. 소유자만 변경 가능.

```
@external
def join_event(self, _join_message:int) -> None:
```
- 참여시 옵셔널한 값을 _join_message로 입력받고 이벤트에 참여한다.

```
@external
def raffle(self) -> str:
```
- 소유자만 수행 가능. 이벤트 당첨자를 선택. 한번에 한명의 당첨자를 뽑는다.
  
```
@external(readonly=True)
def count_join_user(self) -> str:
```
- 이벤트 참여자 수를 출력한다.

```
@external(readonly=True)
def show_event_winner(self) -> str:
```
- 이벤트 당첨자 수와 당첨자의 지갑 주소를 출력한다.

```
@external(readonly=True)
def check_join_message(self, _join_address:str = None) -> str:
```
- 참여자의 옵셔널한 응답 값을 확인할 수 있음. 조회하는 지갑주소가 없을 경우 트랜잭션을 발생시킨 본인의 응답 값을 반환하며 
  조회할 지갑 주소를 _join_address로 입력하면 이벤트 참여시 입력했던 메세지를 출력한다.
```
@external(readonly=True)
def check_event_state(self) -> str:
```
- 현재 이벤트의 open/close 상태를 출력한다.
***

# Author
> nomadconnection Techsupport TEAM. (bjlee)
