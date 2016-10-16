(* James Lynn CSE 307 Homework 3 *)
(* Brackets *)

fun checkInput(L) = 
	if L = [] then 0
	else if hd(L) = 1 then 1 + checkInput(tl(L))
	else ~1 + checkInput(tl(L));

fun brackets(L) =
	if L = [] then false
	else if checkInput(L) = 0 then true
	else false;
    
brackets([0,1]);
