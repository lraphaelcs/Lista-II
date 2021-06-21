from room import Room
from path_finder_agents import RandAgent, BBAgent, BFSAgent, DFSAgent, GreedyAgent

# env = Room(room=[[0, 0, 1], [0, 0, 1], [0, 0, 0]], target=[2, 2])
env = Room(prob=0.2, n=10, plot_on=True)
# agent = RandAgent(env)
# agent = BFSAgent(env)
# agent = DFSAgent(env)
# agent = AStarAgent(env)
agent = GreedyAgent(env)
# gent = BBAgent(env,bound=20)

agent.run()
input('Press ENTER to get out of here')
