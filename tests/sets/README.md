Test cases for traditional connect four settings.
Every file contains on each of the 1000 lines "board evaluation".

set     state     difficulty   nb movecsmoves       nb remaining moves
s3d1    end       easy         28 < moves                 remaining < 14
s2d1    middle    easy         14 < moves <= 28           remaining < 14
s2d2    middle    medium       14 < moves <= 28     14 <= remaining < 28
s1d1    begin     easy              moves <= 14           remaining < 14
s1d2    begin     medium            moves <= 14     14 <= remaining < 28
s1d3    begin     hard              moves <= 14     28 <= remaining
