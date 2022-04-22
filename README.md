# webppl-cognitive-agents

This is a WebPPL library for modelling *cognitive agents* 
interacting in an environment we call *cognitive stochastic 
multiplayer game*. The library currently supports (i) *construction* of 
cognitive models, (ii) *simulating* their execution, (iii) as well as 
*inferring* characteristics of cognitive agents from data. 

## Background (theoretical)
Our framework is based on standard constructs
from game theory, such as expected utility, rationality or discounted
rewards, but its novelty has to do with capturing what really 
motivates (predominantly human) decision makers and how they
deal with arising *uncertainty*. In particular, we hypothesise 
that, besides the usual physical rewards, such as money, time, 
fast car or new dress, humans also care about less tangible things,
like sustaining interpersonal relations, conforming to social norms,
maximising happiness and avoiding negative emotions. These *mental 
attitudes* pose various modelling challenges; it's not clear how to
quantify them, and it's not realistic to treat their values as 
public information. 

The way we handle it is by defining a set of 
*mental attitudes* that give rise to *mental
rewards*, which are accumulated by agents during execution of the 
game along with standard, physical rewards. Each mental attitude induces a
*mental state* for each agent, which specifies the value of an 
attitude at a given time. Since agents can't directly observe 
mental states of their opponents, they use heuristics, which we call
*dynamics functions*, to estimate them. An agent might be motivated
by maximising the value of their own mental states (which they know),
or someone else's (which they estimate), reflected in their utility 
function, which is a linear combination of physical and mental
rewards. 

## Code Overview
The meat of the library is the top level of the ``src`` directory 
which contains the following files:
* ``cognitiveAgent.wppl`` implements the decision-making process of 
cognitive agents
* ``cognitiveGame.wppl`` implements the cognitive stochastic 
multiplayer game model 
* ``simulate.wppl`` contains scaffold code for running simulations
* ``infer.wppl`` contains scaffold code for running inferences

There are also several auxiliary files in the ``aux`` subdirectory:
* ``lambdas.wppl`` contains definitions of some trivial functions,
so they can be used as lambdas in HOFs like maps and folds (called 
``reduce`` here)
* ``logging.wppl`` implements a basic logging mechanism
* ``array.wppl`` provides a variety of utility functions that operate
  on arrays
* ``assert.wppl`` implements a basic assertion mechanism
* ``auxiliary.wppl`` collects various helper functions that do not fit 
  into any category
* ``metaParams.wppl`` provides utility functions that abstract away the
  implementation details of meta-parameters
* ``printing.wppl`` implements printing for various objects (needed
because webppl doesn't print objects when used inline)
* ``belief.wppl`` collects functions that operate on beliefs; it 
effectively hides the complexity of different belief representations,
providing a uniform interface

Next, the ``templates`` directory includes templates for defining (i) an 
instance of a cognitive stochastic game (``gameTemplate.wppl``) and (ii) a
set of simulation scenarios (``simulationTemplate.wppl``).
Apart from the templates, numerous examples are included in the ``examples`` 
directory.

Finally, some tests are defined in the ``test`` directory; most notably,
``integration.wppl`` defines a set of games of increasing complexity, 
simulates their execution and checks that the traces are as expected. 
It is designed as a comprehensive test with high codebase coverage.
Note that the tests are made into a node package (by including a 
``package.json`` file) so that common code may be placed in a separate
file (``util.wppl``) which is then used by various test files.

## Installation
To use the ``webppl-cognitive-agents`` package, a running installation of
``webppl`` is required, which in turn requires Node.js to be present.

Follow instructions from WebPPL documentation, available at 
https://webppl.readthedocs.io/en/master/installation.html to install
Node.js and WebPPL. 

Then, ``webppl-cognitive-agents`` package is installed like any other 
Node package:
```
npm install webppl-cognitive-agents
```

To verify the installation was successful, execute <br/>
```
webppl test/installation.wppl --require .
```
from the root of the installed package. 

## Usage
A typical workflow of using the library will follow the structure
of provided examples. In particular, one must specify the mechanics
of the modeled scenario, which takes form of a function that defines
all the standard (and non-standard) game components. The convention
followed throughout ``examples`` directory is that this function is
defined in a ``<name-of-scenario>.wppl`` file. 

To do something useful with the defined model, one would typically (i) 
define a set of scenarios (i.e., agents' parameters and initial states
along with game parameters) and simulate their execution and/or (ii) 
in presence of behavioural data, use that data to infer characteristics
of the involved agents.

__Note__: each example is made into a separate webppl package (achieved by
including ``package.json`` in each example directory). That's for a
technical reason - WebPPL doesn't seem to have a mechanism for 
*including* files and so if we want to split the code into 
multiple files, creating a package is the only way I found of 
making it work. Assuming you have added your example to ``examples``
directory, to run the experiments from the top-level directory
(``webppl-cognitive-agents``), you would execute
```
$ webppl examples/<exampleName>/src/simulations.wppl --require . --require examples/<exampleName>/ [--] [--experiment <experimentID>] [--scenario <scenarioID>]
```  
So besides including the ``webppl-cognitive-agents`` package, you must also 
include your example.

As mentioned above, the experiments will be either (i) simulating 
model execution or (ii) learning agents' characteristics based on 
data, but regardless of the type of experiment, the model itself
must be defined in the same way. Below, we formally outline
how such a model is specified.

### Defining the Model
The main thing is to define game setup, specifying the usual stuff 
such as states, actions, 
transition function as well as game API (described below), plus
novel components to do with rewards. Game setup should be specified
as a function which accepts an object with game-specific parameters 
(which differ for every game) as input and
returns an object (dictionary) containing the following fields:
+ ``actions :: State -> [Action]`` <br/>
a function that retrieves **actions** available to an agent
in a given *state*
+ ``transitionFn :: (State, Action) -> State`` <br/>
a function that gives a **state** to which the game transitions
given that *action* was taken in a *state*
+ ``initialState :: State``
+ ``API :: Object`` 
specifies definitions of several functions which are used by the
library, but their implementations are game-specific, such as
    + ``getPreviousState :: State -> State`` <br/>
    given a *state*, returns a **state** that preceded *state* in
    the execution of the game. Normally states encode execution
    histories, so implementation of this function is trivial
    + ``getLastAction :: State -> Action``
    + ``endsRound :: State -> Action -> Bool`` (optional) <br/>
    does *action* taken in a *state* end the round?; the notion of a round
    is introduced to allow control of timeframes when discounting 
    happens
    + ``isInitial :: State``
    + ``turn :: State -> Agent`` <br/>
    retrieves an **agent** that takes action in (owns) a given 
    *state* 
    + ``stateToString :: State -> String`` <br/>
    how to print states
    + ``actionSimilarity :: State -> Action -> Number`` (optional)
    provides a notion of similarity between actions, measured as a 
    nonpositive distance; by default, distance is 0 for same actions and
    -100 for different actions. In general, the lower the score, the more
    dissimilar the actions are. A custom similarity measure may be
    especially useful when actions are numbers. It is used for making
    inferences about agent's characteristics when updating (discrete) belief
    
     
+ ``physicalRewardStructure :: Object`` <br/>
captures action and state rewards of agents. Must contain following 
fields:
    + ``stateRewards :: State -> [[Number]]`` <br/>
    Given a state, returns an array (indexed by agentID) whose ith
    element is an array of rewards obtained by agent i in that state.
    The length of this array of rewards should be equal to 
    params.numberOfRewards.physical (see below). 
    + ``actionRewards :: State -> [[Number]]`` <br/>
    As above, but returns rewards obtained from taking an action.
+ ``mentalStateDynamics :: Object`` <br/>
captures the mental reward component of the utility function - that 
involves providing estimation heuristic for each mental state
as well as a way to compute each mental state. One must also 
specify the mental component of each agent's utility function.
Therefore, this object must contain the following fields:
    + ``estimationHeuristicArr :: [Function]`` <br/>
    array of functions expressing heuristics for each mental
    attitude. The length of the array should be equal to the 
    number of mental attitudes, i.e. equal to 
    ``params.numberOfRewards.mental``. Each function should have
    the following signature:
    ```
    Value -> AgentID -> AgentID -> Belief -> State -> Action
    ```
    where the arguments are as follows:
        + ``prevValue :: Value`` is the previous value (before 
        ``action`` is taken at ``state`` [see below]) of the mental
        state; usually, ``Value = Double``
        + ``estimatingAgentID :: AgentID`` identifies an agent
        who is estimating the value of this mental state
        + ``estimatedAgentID :: AgentID`` identifies an agent
        whose mental state is being estimated
        + ``state :: State``
    Overall, each heuristic is a function that captures how 
    ``estimatorAgentID``'s estimation of ``estimateeAgentID``'s
    mental state changed from ``prevValue`` upon ``action`` taken
    in ``state``, given ``estimatorAgentID``'s ``belief`` 
    + ``mentalStateArr :: [Function]`` <br/>
    an array with the same dimensions as ``estimationHeuristicArr``,
    but containing functions that *compute* (rather than *estimate*)
    mental state of agents. It captures how agents feel. Each 
    function should have the following signature:
    ```
        AgentID -> Belief -> State -> Value
    ```
    where each function computes ``agentID :: AgentID``'s mental state 
    in ``state :: State`` given their ``belief :: Belief``. Note
    that this computation is only available to agent identified by
    ``agentID``. Typically ``Value = Double`` of course.
    + ``mentalUtilities :: [[[Int]]]`` <br/>
    captures mental utilities of each agent, indexed by agentID.
    Each element is an array indexed by mental attitudes (we assume
    they're ordered and indexed as 0,1,2,...) and the elements
    of that array are... arrays containing agentIDs, identifying
    agents whose mental state an agent cares about. It's easier
    to understand on an example. Take a game with two mental 
    attitudes (trust and guilt) and two agents (alice, bob).
    The order here matters, so trust is mental attitude index 0,
    guilt index 1, alice is agent with agentID=0, bob has ID 1.
    Then, the following mentalUtilities array
    ```javascript
    [
    [[1],[0]], /** mental utility of agent 0 - alice */
    [[0,1],[1]], /** mental utility of agent 1 - bob */
    ]
    ```
    would reflect that 
    + alice cares about bob's trust ([1])
    + alice cares about her own guilt ([0])  
    + bob cares about alice's as well as his own trust ([0,1])
    + bob cares about his own guilt ([1])  
+ ``params :: Object`` <br/>
must contain the following basic information about the game:
    + ``numberOfAgents :: Int``
    + ``numberOfRewards :: Object``, consisting of
        + ``physical :: Int``
        + ``mental :: Int``
+ ``rewardUtilityFunctions :: Object`` a set of functions, one per
  reward, that form part of the utility function, split into physical
  and mental:
  + ``physical :: [Function]`` ordered array of reward utility
  functions for physical rewards
  + ``mental :: [Function]`` ordered array or reward utility
  function for mental rewards
+ ``heuristics :: Object`` (optional)
An optional specification of heuristics that agents use to guess
actions of their opponents and/or update their belief following
opponents' actions. Contains the following fields:
  + ``action :: Object`` (optional)
  + ``belief :: Object`` (optional)
which specify the action and belief heuristics, respectively.
Both elements have the same structure, consisting of a _filter_
function that controls when the heuristic applies and the _compute_
function that encodes the actual heuristic. Both elements are optional.

### Running Simulations
To simulate the execution of a model, one must specify a **scenario**,
which, besides some basic parameters, specifies the characteristics 
and initial state of agents. In particular, each scenario is an object
(dictionary) consisting of the following fields:
+ ``name :: String`` <br/>
the name of the scenario, or a short description
+ ``options :: Object``, consisting of
    + ``horizon :: Int`` <br/>
    how many steps to run the simulation for 
    + ``beliefRepresentation :: String`` <br/>
    either ``discrete`` or ``dirichlet``
+ ``gameSpecificParams :: Object`` <br/>
custom object; it is passed to the function that constructs game
structure (see above)
+ ``agents :: [Object]`` <br/>
most substantial component of a scenario; defines parameters and 
initial state of agents; each element of this array represents an 
agent and consists of:
    + ``params :: Object``, consisting of
        + ``goalCoeffs :: [Double]`` <br/>
        an array of coefficients that should sum to 1; the length 
        should be equal to 
        ``numberOfRewards.phyiscal + numberOfRewards.mental``
        + ``metaParams :: Object`` sets meta-parameters of an agent:
            + ``alpha :: Double`` <br/>
            rationality of an agent; a nonnegative real number where
            0 means completely random actions and > 100 is (almost)
            perfect rationality
            + ``discountFactor :: Double`` <br/>
            how much an agent discounts future rewards: a real 
            number between 0 (only cares about now) and 1 (no 
            discounting) 
            + ``lookAhead :: Int`` <br/>
            how far an agent looks into the future
    + ``initialState :: Object``, consisting of
        + ``belief :: [Belief]`` <br/>
        array of beliefs over each agent (including oneself); length
        should be equal to ``numberOfAgents``; each belief is either
        (i) a distribution over goal coefficient vectors (when 
        ``discrete`` representation used) or (ii) an array of 
        parameters (when ``dirichlet`` representation used)
        + ``mentalEstimations :: [[Distribution]]`` <br/>
        array of estimations of each agent's (including oneself)
        mental states; those estimations are distribution objects
        + ``metaParamsEstimations :: Object``, consisting of
            + ``alpha :: [Distribution]``
            + ``lookAhead :: [Distribution]``
            + ``discountFactor :: [Distribution]`` <br/>
            each of the above is an array of estimations of one of 
            meta-parameters of each agent (including oneself, which
            should be ``null``)
    
          
See ``test/integration.wppl`` and ``examples`` directory for 
examples of scenarios.