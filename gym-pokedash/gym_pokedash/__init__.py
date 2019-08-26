import gym
from gym.envs.registration import register

env_name = 'PokeDash-v0'
if env_name in gym.envs.registry.env_specs:
    del gym.envs.registry.env_specs[env_name]

register(
    id='PokeDash-v0',
    entry_point='gym_pokedash.envs:PokeDashEnv',
)