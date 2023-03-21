import math

def state_quality(states: dict[dict], country: str, resources: dict[dict]):
    ret_value = 0
    for resource in resources:

        # check if this is a tiered weight/factor resource
        # if so then use the appropriate tiered weight
        if (resources[resource]['Weight'].count(';') > 0):
            temp_weights = resources[resource]['Weight'].split(';')
            temp_factors = resources[resource]['Factor'].split(';')
            for index in range(len(temp_factors)):
                if (float(states[country][resource]) / float(states[country]['Population']) < float(
                        temp_factors[index])):
                    break
            print(resource + " - " + str(
                float(states[country][resource]) / float(states[country]['Population']) * float(temp_weights[index])))
            ret_value += float(states[country][resource]) / float(states[country]['Population']) * float(
                temp_weights[index])

        # default value: resource/popultation * weight
        else:
            print(resource + " - " + str(
                float(states[country][resource]) / float(states[country]['Population']) * float(
                    resources[resource]['Weight'])))
            ret_value += float(states[country][resource]) / float(states[country]['Population']) * float(
                resources[resource]['Weight'])
    return ret_value


# The undiscounted reward is the state_quality of a state minus the state_quality of the inital state
def undiscounted_reward(state_quality1: float, state_quality2: float) -> float:
    # current node's state quality - initial_state_quality
    return state_quality2 - state_quality1


# The discounted reward is the undiscounted_reward * gammaa^depth
def discounted_reward(reward: float, N: int) -> float:
    # start with gamma of 0.5 since gamma needs to be 0<=gamma<1
    gamma = 0.5
    return gamma ^ N * reward


def country_accept( country: str, state: dict[dict], resources: dict[dict], init_states: dict[dict], depth) -> float:
    k = 1
    x = 0

    # state quality of country
    sq = state_quality(state, country, resources)
    # original state quality of country
    og_sq = state_quality(init_states, country, resources)

    # undiscounted reward
    ur = undiscounted_reward(og_sq, sq)

    # discounted reward
    dr = discounted_reward(ur, depth )

    expon = -k * ( dr - x)
    return (1 / (1+ math.exp(expon)))

def success_probability(state: dict[dict], resources: dict[dict], init_states: dict[dict], depth) -> float:
    ret_val = 1
    for country in state:
        ret_val *= country_accept(country, state, resources, init_states, depth)
    return ret_val

def expected_utility(country: str, state: dict[dict], resources: dict[dict], init_states: dict[dict], schedule: list) -> float:

    # negative constant for failure case
    # starting with -0.5 to see results
    neg_C = -0.5

    depth = len(schedule)
    # state quality of country
    sq = state_quality(state, country, resources)
    # original state quality of country
    og_sq = state_quality(init_states, country, resources)

    # undiscounted reward
    ur = undiscounted_reward(og_sq, sq)

    # discounted reward
    dr = discounted_reward(ur, depth)

    # check if the latest Action is a (transfOrm or transfEr
    # if TRANSFORM then send back self discounted reward
    if schedule[len(schedule)-1]['Action'][7] == 'O':
        return dr
    else:
        prob_success = success_probability(state, resources, init_states, depth)
        eu = (prob_success * dr)+((1-prob_success)*neg_C)
        return eu
