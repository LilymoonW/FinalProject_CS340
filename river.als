--Variable declarations ---
abstract sig Item{}

one sig Farmer, Wolf, Goat, Cabbage extends Item{}

var sig ThisSide in Item{}
var sig OtherSide in Item{}

---the initial setup of everything---

// We want everything to start on this side
pred init(ts: ThisSide, os: OtherSide){
	no os
	ts = Item
}

// want everything to eecntually be on the other side 
fact eventuallyAllOtherSide{
	eventually OtherSide = Item
}


//do nothing 
pred doNothing{
	ThisSide' = ThisSide
	OtherSide' = OtherSide
}

fact validTraces{
	init[ThisSide, OtherSide]
	always{
		// force progress something or nothing crosses but farmer has to move back and forth
		(OtherSide != Item) =>(crossOtherToThis[Goat] or crossThisToOther[none] or crossThisToOther[Goat] or crossOtherToThis[none] or crossThisToOther[Wolf] or crossOtherToThis[Wolf]  or crossThisToOther[Cabbage] or crossOtherToThis[Cabbage] )
	
		// only when it is true that they are on the otehr side can they do nothing afterwards when everyone is on the other side
		(OtherSide = Item) => doNothing
	}
}

--predicates----

//cross forwards
pred crossThisToOther(i: Item){
	//preconditions
	Farmer in ThisSide
	i in ThisSide
	
	//actions being done
	ThisSide' = ThisSide - Farmer - i
	OtherSide' = OtherSide + Farmer + i
}

//cross backwards
pred crossOtherToThis(i: Item){
	//preconditions
	Farmer in OtherSide
	i in OtherSide

	//actions being done
	ThisSide' = ThisSide + Farmer + i
	OtherSide' = OtherSide - Farmer - i
}


//cannot have the goat be alone with cabbage and the goat cannot bewith the wolf
fact rules{
	always{
		// goat can't be alone with cabbage
		(Farmer in ThisSide and Goat in OtherSide) => not(Cabbage in OtherSide)
		(Farmer in OtherSide and Goat in ThisSide) => not(Cabbage in ThisSide)
		
		//goat acna't be with wofl
		(Farmer in ThisSide and Goat in OtherSide) => not(Wolf in OtherSide)
		(Farmer in OtherSide and Goat in ThisSide) => not(Wolf in ThisSide)
		}
}

run{} for 7















