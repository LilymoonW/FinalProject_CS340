-start off with like the variable states--
abstract sig Jug{
	var amount: Int,
	capacity: Int,
	var whichStep: Step
}
one sig Jug1, Jug2 extends Jug{}
one sig TargetAmount{
	value: Int
}


abstract sig Step{}
one sig Fill, Empty, Pour, Nothing extends Step{}


-intial constraints from problem statement--
fact constraints{
	Jug1.capacity > 0
	Jug2.capacity > 0
	TargetAmount.value > 0
	TargetAmount.value < Jug1.capacity or TargetAmount.value < Jug2.capacity
}

pred init{
	all j: Jug | j.amount = 0 and j.whichStep = Nothing
} 
//the  is reached by some jug
pred target{
	some j: Jug | j.amount = TargetAmount.value
}

fact validTraces{
	init
	always{
		// you can only do nothing once the target is reached by some jug
			not target => (some j: Jug | fill[j] or empty[j])and (lone j: Jug | not doesNothing[j])
			or 
			target => all j: Jug | doesNothing[j]
		
	}
}

--- the actual things you can do----
pred fill(j: Jug){
	//precondition
	j.amount < j.capacity 
	j.amount' = j.capacity
	all other: Jug - j | other.amount' = other.amount

	//step change
	j.whichStep = Fill
}

pred empty(j:Jug){
	//precondition
	j.amount > 0

	j.amount' = 0
	all other: Jug - j | other.amount' = other.amount
	j.whichStep = Empty
}

pred doesNothing[j: Jug]{
	j.amount' = j.amount
	j.whichStep = Nothing
	all other: Jug - j  | other.amount' = other.amount
}

assert oneJugAtATime{
	always {lone j: Jug | j.whichStep != Nothing}
} check oneJugAtATime


run {} for 5





















