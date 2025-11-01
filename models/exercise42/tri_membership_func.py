from dataclasses import dataclass

@dataclass
class TriMembershipFunc:
    name:str
    left_point: int   
    center_point: int 
    right_point: int  