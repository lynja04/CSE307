fun deleteIndex(L, x) =
    if L = [] then []
    else if hd(L) = x then delete(L, )
fun removeFirst(L) =
		tl(L);
(* Where X is the length-1 *)
fun removeLast(L, x) =
		if x = 0 then []
    else if hd(tl(L)) = 1 then deleteIndex(L, x)
		else hd(L)::removeLast(tl(L), x-1);
fun trim(L) =
		removeLast((removeFirst(L), length(removeFirst(L))-1));


fun stuff(L) =
    trim(L);

stuff([0,0,1,0,0,1,1,1]);
