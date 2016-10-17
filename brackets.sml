(* James Lynn CSE 307 Homework 3 *)
(* Brackets *)

(* The algorithm:
		Read the list until total is 0.
		Get the highest positive number as the height.
		Get the length - 1 as the Width
		Calculate the area
		Delete first 0 in that list and it's closing 1
		Repeat and alternate adding/subtracting area *)

(* height and width methods *)
(* Get the height of the List, which is the highest positive number *)
fun height(L) =
		if hd(L) = 1 then 0
		else 1 + height(tl(L));
(* Get Width of the List, which is length - 1 *)
fun width(L) =
		length(L)-1;
fun length(L) =
		if L = [] then 0
		else 1 + length(tl(L));
(****************************)

(* Remove first and list element of the list *)
fun removeFirst(L) =
		tl(L);
(* Where X is the length-1 *)
fun removeLast(L, x) =
		if x = 0 then []
		else hd(L)::removeLast(tl(L), x-1);
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

(* Helper Helper *)
fun helpTheHelper(L, index) =
		if hd(L) = [] then 0
		else if index mod 2 = 0 then (width(L)*height(L))-helpTheHelper(removeLast((removeFirst(L), length(removeFirst(L))-1)), index+1)
		else (width(L)*height(L))+helpTheHelper(removeLast((removeFirst(L), length(removeFirst(L))-1)), index+1)
(****************************)

(* Brackets Helper *)
fun bracketsHelper(L) =
		if L = [] then 0
		else helpTheHelper(hd(L), 0) + bracketsHelper(tl(L));
(****************************)

(* Main function *)
fun brackets(L) =
		bracketsHelper(createListsofList(L, [], 0));

brackets([0,0,0,1,1,1]);
