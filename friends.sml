(* James Lynn CSE 307 Homework 3 *)
(* Friends *)

fun insert_all(E,L) =
    if L=[] then []
    else (E::hd(L)) :: insert_all(E,tl(L));

insert_all(1,[[],[2],[3],[2,3]]);

fun powerSet(L) =
    if L=[] then [[]]
    else powerSet(tl(L)) @ insert_all(hd(L),powerSet(tl(L)));

powerSet([]);
powerSet([1,2,3]);
powerSet([2,3]);
