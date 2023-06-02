from gyms.envs.engine import Engine

def main():
    env = Engine()
    net = None
    done = False
    loss_history = []
    epoch_history = []
    observation = env.reset()
    while not done:
        action = net.choose_action(observation)
        n_state, state, info, done = env.step(action)
        #Calculate loss
        net.store_transition
        #Set new current observation
        observation = n_state

if __name__ == '__main__':
    pass
