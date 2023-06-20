import numpy as np

'''
Agent Memory
'''
class MemoryBuffer(object):
    '''
    :key max_mem_size int max memory before overwritting old memories
    :key input_shape Tensor Shape of the input Tensor
    :key n_actions int Number of actions available
    '''

    def __init__(self, max_mem_size, input_shape, n_actions):
        # Max memory
        self.max_mem = max_mem_size
        # Number of actions
        self.n_actions = n_actions
        # Counter to keep track of what memory we are on
        self.mem_counter = 0
        # Memory of the current state
        self.state_memory = np.zeros((self.max_mem, *input_shape), dtype=np.float32)
        # Memory of the next state
        self.n_state_memory = np.zeros((self.max_mem, *input_shape))
        # Memory of actions taken
        self.action_memory = np.zeros((self.max_mem, n_actions))
        # Memory of rewards
        self.reward_memory = np.zeros(self.max_mem)
        # Memory of terminal
        self.terminal_memory = np.zeros(self.max_mem, dtype=np.bool)
    '''
    :key state <T> current state
    :key action <T> action taken
    :key reward float reward from env
    :key n_state <T> next state
    :key done int done value
    :return void
    '''

    def store_transition(self, state, action, reward, n_state, done):
        # Current memory index
        index = self.mem_counter % self.max_mem
        # Update memory
        self.state_memory[index] = state
        self.n_state_memory[index] = n_state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.reward_memory[index] = done
        # increment counter
        self.mem_counter += 1

    '''
    :key batch_size int size of the memory batch
    :return list
    '''

    def sample_buffer(self, batch_size):
        # Get current index or max index
        batch = min(self.mem_counter, self.max_mem)
        # Random sample index
        index = np.random.choice(self.max_mem, batch)
        # Values from that sample index
        state = self.state_memory[index]
        n_state = self.n_state_memory[index]
        action = self.action_memory[index]
        reward = self.reward_memory[index]
        done = self.terminal_memory[index]

        return state, reward, action, n_state, done
    def can_sample(self):
        return self.mem_counter >= self.max_mem