(* James Lynn CSE 307 Homework 3 *)
(* Brackets *)

(* height, width and area methods *)
(* Get the height of the List, which is the highest positive number *)
fun max(L, x) =
		if L = [] then x
		else if hd(L) > x then max(tl(L), hd(L))
		else max(tl(L), x);
fun height(L, x) =
		if L = [] then []
		else if hd(L) = 0 then x+1::height(tl(L), x+1)
		else x-1::height(tl(L), x-1);
(* Get Width of the List, which is length - 1 *)
fun width(L) =
		length(L)-1;
fun length(L) =
		if L = [] then 0
		else 1 + length(tl(L));
fun area(L) =
		width(L) * max(height(L, 0), ~1);
(****************************)

(* Remove first and list element of the list *)
fun removeFirst(L) =
		tl(L);
(* Where X is the length-1 *)
fun removeLast(L, x) =
		if x = 0 then []
		else hd(L)::removeLast(tl(L), x-1);
fun trim(L) =
		removeLast((removeFirst(L), length(removeFirst(L))-1));
(****************************)

(* Lists of lists methods *)
(* Break the list into multiple structures *)
fun reverse(L) =
   	if L = [] then []
	  else reverse(tl(L)) @ [hd(L)];

fun createListsofList(L, prefix, x) =
		if L = [] then [prefix]
		else if hd(L) = 0 then createListsofList(tl(L), hd(L)::prefix, x+1)
		else if hd(L) = 1 andalso x = 1 then reverse((hd(L)::prefix))::createListsofList(tl(L), [], 0)
		else createListsofList(tl(L), hd(L)::prefix, x-1);
(****************************)

(* Check if all the lists in the list are empty *)
fun checkIfListEmpty(L) =
		if L = [] then true
		else if hd(L) <> [] then false
		else checkIfListEmpty(tl(L));
(****************************)

(* Get the area of all the lists within the list *)
fun areaOfWholeList(L, sign) =
		if checkIfListEmpty(L) = true then 0
		else if hd(L) = [] then areaOfWholeList(tl(L), sign)
		else if sign = 0 then area(hd(L)) + areaOfWholeList(tl(L), 0)
		else ~(area(hd(L))) + areaOfWholeList(tl(L), 1);
(****************************)

(* Helpers the helper by triming and breaking into more lists *)
fun helperHelper(L) =
		if checkIfListEmpty(L) = true then []
		else if hd(L) = [] then helperHelper(tl(L))
		else createListsofList(trim(hd(L)), [], 0) @ helperHelper(tl(L));
(****************************)

(* Brackets Helper *)
fun bracketsHelper(L, sign) =
		if L = [] then 0
		else if sign = 0 then areaOfWholeList(L, 0) + bracketsHelper(helperHelper(L), 1)
		else areaOfWholeList(L, 1) + bracketsHelper(helperHelper(L), 0);
(****************************)

(* Main function *)
fun brackets(L) =
		bracketsHelper(createListsofList(L, [], 0), 0);
(****************************)

brackets([0,0,1,1,0,0,1,0,0,1,1,1]);
