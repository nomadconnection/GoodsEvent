from iconservice import *

TAG = 'GoodsEvent'

class GoodsEvent(IconScoreBase):

    _EVENT_STATE  = 'event_state'
    _JOIN_MESSAGE = 'join_message'
    _JOIN_ADDRESS = 'join_address'
    _EVENT_WINNER = 'event_winner'
    
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        # True:Event OPEN / False:Event CLOSE
        self._VDB_event_state = VarDB(self._EVENT_STATE, db, value_type=bool)
        # {ADDRESS:Answer Optional Message(exam. 1 ~ 5)}
        self._DDB_join_message = DictDB(self._JOIN_MESSAGE, db, value_type=int)
        # [ADDRESS_1, ADDRESS_2, ...] -> Not to be duplicate address
        self._ADB_join_address = ArrayDB(self._JOIN_ADDRESS, db, value_type=str)
        # event_winner array(list) point
        self._ADB_event_winner = ArrayDB(self._EVENT_WINNER, db, value_type=int)
        
    def on_install(self) -> None:
        super().on_install()
        self._VDB_event_state.set(False)
        
    def on_update(self) -> None:
        super().on_update()
        
    def owner_check(self) -> None:
        if self.msg.sender != self.owner:
            revert('Permission Deny.')
    
    def random_range(self, _range:int, _paste_cnt:int=0) -> int:
        if _range < 0: return 0
        
        _txhash = str(int.from_bytes(self.tx.hash, byteorder='big', signed=False))
        _paste_dt = _txhash + _txhash[0:_paste_cnt]
        
        return int(_paste_dt) % _range
        
    @external
    def event_start(self) -> None:
        self.owner_check()
        self._VDB_event_state.set(True)
    
    @external
    def event_stop(self) -> None:
        self.owner_check()
        self._VDB_event_state.set(False)
    
    @external
    def join_event(self, _join_message:int) -> None:
        if not self._VDB_event_state.get(): revert('Event Closed.')
        
        #init
        self._ADB_join_address = ArrayDB(self._JOIN_ADDRESS, self.db, value_type=str)
        
        if _join_message < 1 or _join_message > 5:
            revert('Check your Message Value...')
        
        _sender_address = str(self.msg.sender)
        
        if self._DDB_join_message[_sender_address] == 0:
            self._ADB_join_address.put(_sender_address)
            
        self._DDB_join_message[_sender_address] = _join_message
        
    @external
    def raffle(self) -> str:
        self.owner_check()
        
        if self._VDB_event_state.get(): revert('Please close the event first.')
        
        #init
        self._ADB_join_address = ArrayDB(self._JOIN_ADDRESS, self.db, value_type=str)
        self._ADB_event_winner = ArrayDB(self._EVENT_WINNER, self.db, value_type=int)
            
        _join_count = len(self._ADB_join_address)
        
        if _join_count == 0: revert('Candidate list is empty.')
        
        _bef_cnt = len(self._ADB_event_winner)
        
        for cnt in range(0, 10):
            _get_random = self.random_range(_join_count, cnt)
            
            if _get_random in self._ADB_event_winner: continue
            
            self._ADB_event_winner.put(_get_random)
            
            _get_address = self._ADB_join_address[_get_random]
            
            break
        
        if _bef_cnt == len(self._ADB_event_winner):
            revert("Sorry... There is a lot of redundancy and can not be selected.")
        
    @external(readonly=True)
    def count_join_user(self) -> str:
        #init
        self._ADB_join_address = ArrayDB(self._JOIN_ADDRESS, self.db, value_type=str)
        return str(len(self._ADB_join_address))
        
    @external(readonly=True)
    def show_event_winner(self) -> str:
        #init
        self._ADB_join_address = ArrayDB(self._JOIN_ADDRESS, self.db, value_type=str)
        self._ADB_event_winner = ArrayDB(self._EVENT_WINNER, self.db, value_type=int)
        
        return "Count=[%s], Address LIST=%s"\
               %(str(len(self._ADB_event_winner)),\
                 str(list(map(lambda p: self._ADB_join_address[p], self._ADB_event_winner))))
        
    @external(readonly=True)
    def check_join_message(self, _join_address:str = None) -> str:
        if not _join_address: _join_address = str(self.msg.sender)
        
        _get_msg = self._DDB_join_message[_join_address]
        
        if _get_msg == 0: return "Address(%s) is not join event."%(_join_address)
        
        return str(_get_msg)
        
    @external(readonly=True)
    def check_event_state(self) -> str:
        if self._VDB_event_state.get(): return "Event OPEN."
        
        return "Event CLOSE."
        
