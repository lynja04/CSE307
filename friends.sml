(* James Lynn CSE 307 Homework 3 *)
(* Friends *)

fun insert_all(E,L) =
    if L=[] then []
    else (E::hd(L)) :: insert_all(E,tl(L));

insert_all(1,[[],[2],[3],[2,3]]);

fun powerSet(L) =
    if L=[] then [[]]
    else powerSet(tl(L)) @ insert_all(hd(L),powerSet(tl(L)));

fun survey(numOfPeople, listOfIntroProtocols, confidences) =
    


survey(6,[(1,0,0), (2,0,1), (3,1,2), (4,2,1), (5,0,0)], [13,3,6,20,10,15]);
