This file provides an overview of the functionality of the trust game webppl model. 

There are two important functions that the module offers:
* makeTrustCSMG(params)
** input: params is a dictionary of the following format 

E.g. 
var params = {
  endowments : {
    'investor': 0,
    'investee': 0
  },
  k: 0,
  horizon: 0
}
var csmg = makeTrustCSMG(params)

where csmg is an object of the following format
{
	actions,
	transition,
	initialState,
	params
}

* makeAgent(params) e.g.

var selfParams = {
 alpha: [0,inf),
 moneyWeight: [0,1],
 trustWeight:  [0,1],
 role: 'investor'/'investee'
 initialBelief: {
  alpha: <dist>,
  moneyWeight: <dist>,
  trustWeight: <dist>
 }
}

var agent = makeAgent(params)

agent is an object such as
{ 
	params: selfParams, 
	act, 
	expectedUtility, 
	updateBelief
}

State consists of:
* turn: indicates whether next move is investing or returning
* timeLeft: how many time steps are left in the game 
* investments: history of amounts sent by investor
* returns: history of amounts sent by investee
* endowments: a dictionary {'investor': x, 'investee': y} specifying
how much both players received in endowments in this stage
