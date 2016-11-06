(* James Lynn CSE 307 Homework 3 *)
(* Friends *)

(* Power Set *)
fun insert_all(E,L) =
		if L=[] then []
		else (E::hd(L)) :: insert_all(E,tl(L));
fun powerSet(L) =
		if L=[] then [[]]
		else powerSet(tl(L)) @ insert_all(hd(L),powerSet(tl(L)));
(********************************)

(* Confidence helpers *)
(*fun getPersonsConfidence(person, confidences, x) =
    if x = person then hd(confidences)
    else getPersonsConfidence(person, tl(confidences), x+1);

fun maxConfidence(listOfConfidences, x) =
    if listOfConfidences = [] then x
    else if hd(listOfConfidences) > x then maxConfidence(tl(listOfConfidences), hd(listOfConfidences))
    else maxConfidence(tl(listOfConfidences), x);

fun createConfidenceEntry(entry, confidences) =
    getPersonsConfidence(hd(entry), confidences, 0)::[getPersonsConfidence(tl(entry), confidences, 0)];

fun createListOfConfidences(filteredList, confidences) =
    if filteredList = [] then []
    else createConfidenceEntry(hd(filteredList), confidences) @ createListOfConfidences(tl(filteredList), confidences);*)
(********************************)

(* Create a list of the people *)
(*fun createListOfPeople(numOfPeople, x) =
    if x = numOfPeople then []
    else x::createListOfPeople(numOfPeople, x+1);*)
(*******************************)

fun addTwo(list) =
		if list = [] then []
		else (2::hd(list))::addTwo(tl(list));

fun getHostFriends(list, host, index) =
		if index = host then hd(list)
		else getHostFriends(tl(list), host, index+1);

fun addFriends(list, listOfFriends, host, index) =
		if listOfFriends = [] then []
		else if index = host then ([hd(listOfFriends)]::hd(list))::addFriends(tl(list), tl(listOfFriends), host, index)
		else addFriends(tl(list), tl(listOfFriends), host, index+1);

fun protocol0(list, host, friend, index) =
		if list = [] then []
		else if index = host then (friend::hd(list))::protocol0(tl(list), host, friend, index+1)
		else if index = friend then (host::hd(list))::protocol0(tl(list), host, friend, index+1)
		else protocol0(tl(list), host, friend, index+1);

fun protocol1(list, host, friend, index) =
		if list = [] then []
		else if index = friend then addFriends(getHostFriends(list, host, 0))::protocol1(tl(list), host, friend, index+1)
		else protocol1(tl(list), host, friend, index+1);

fun parseProtocol(tuple: int*int*int, list) =
		if list = [] then []
		else if #3(tuple) = 0 then protocol0(list, #2(tuple), #1(tuple), 0)
		else if #3(tuple) = 1 then protocol1(list, #2(tuple), #1(tuple), 0)
		(*else if #3(tuple) = 2 then protocol2(list, #2(tuple), #1(tuple), 0)*)
		else parseProtocol(tuple, tl(list));

fun createFriendsList(list, listOfIntroProtocols: (int*int*int) list) =
		if listOfIntroProtocols = [] then []
		else parseProtocol(hd(listOfIntroProtocols), list)@(createFriendsList(list, tl(listOfIntroProtocols)));

fun createStartingList(numOfPeople) =
    if numOfPeople = 0 then []
    else []::createStartingList(numOfPeople-1);

fun surveyHelper(numOfPeople, listOfIntroProtocols, confidences) =
		createFriendsList(createStartingList(numOfPeople), listOfIntroProtocols);

(*******************************)

fun survey(numOfPeople, listOfIntroProtocols, confidences) =
    surveyHelper(numOfPeople, listOfIntroProtocols, confidences);

survey(4,[(1,0,0), (2,1,1), (3,2,0)], [50,25,25,10]);
