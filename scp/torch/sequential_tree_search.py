import numpy as np
from scipy.special import gammainc
import torch
import heapq

def compute_reward(x, xf):
  velIdx = x.shape[0] // 2
  return -(np.linalg.norm(x[0:velIdx] - xf[0:velIdx])) - 0.1 * np.linalg.norm(x[velIdx:] - xf[velIdx])

def state_valid(robot, x, data_neighbors):
  # check if within the space
  if (x < np.array(robot.x_min)).any() or (x > np.array(robot.x_max)).any():
    return False

  # check for collisions with neighbors
  velIdx = x.shape[0] // 2
  for cftype_neighbor, x_neighbor in data_neighbors:
    dist = np.linalg.norm(x[0:velIdx] - x_neighbor.numpy()[0:velIdx])
    if dist < robot.min_distance(cftype_neighbor):
      return False

  return True

# see https://stackoverflow.com/questions/5408276/sampling-uniformly-distributed-random-points-inside-a-spherical-volume
def sample_vector(dim,max_norm,num_points=1):
    r = max_norm
    ndim = dim
    x = np.random.normal(size=(num_points, ndim))
    ssq = np.sum(x**2,axis=1)
    fr = r*gammainc(ndim/2,ssq/2)**(1/ndim)/np.sqrt(ssq)
    frtiled = np.tile(fr.reshape(num_points,1),(1,ndim))
    p = np.multiply(x,frtiled)
    return p

def tree_search(robot, x0, xf, dt, data_neighbors, prop_iter=2, iters=100000, top_k=100, trials=10, cost_limit = 1e6):

  xf = xf.detach().numpy()

  parents = -np.ones((iters,),dtype=np.int)
  states = np.zeros((iters,robot.stateDim))
  states_temp = np.zeros((iters,prop_iter+1,robot.stateDim))
  actions = np.zeros((iters,robot.ctrlDim))
  timesteps = np.zeros((iters,),dtype=np.int)
  reward = np.zeros((iters,))
  cost = np.zeros((iters,))

  for trial in range(trials):
    print("Run trial {} with cost limit {}".format(trial, cost_limit))

    states[0] = x0
    reward[0] = compute_reward(states[0], xf)
    top_k_heap = [(reward[0], 0)] # stores tuples (reward, idx)
    i = 1

    best_reward = reward[0]
    best_i = 0
    best_cost = cost_limit
    sol_x = None
    sol_u = None

    while i < iters:
      # if i % 1000 == 0:
      #   print(i)

      # sample a node to expand
      if np.random.random() < 0.3:
        idx = np.random.randint(0, i)
      else:
        heap_idx = np.random.randint(0, len(top_k_heap))
        idx = top_k_heap[heap_idx][1]

      # randomly sample an action
      # u = np.random.uniform(robot.u_min, robot.u_max)
      u = sample_vector(robot.ctrlDim, robot.g * robot.thrust_to_weight)[0]
      cost[i] = cost[idx] + np.linalg.norm(u)
      if cost[i] > cost_limit:
        continue

      timesteps[i] = timesteps[idx] + prop_iter

      # compute neighbors
      nx_idx = timesteps[idx]
      nx_idx_next = timesteps[i]
      data_neighbors_i = []
      data_neighbors_next = []
      for cftype_neighbor, x_neighbor in data_neighbors:
        if x_neighbor.shape[0] > nx_idx:
          data_neighbors_i.append((cftype_neighbor, x_neighbor[nx_idx,:].detach()))
        else:
          data_neighbors_i.append((cftype_neighbor, x_neighbor[-1,:].detach()))
        if x_neighbor.shape[0] > nx_idx_next:
          data_neighbors_next.append((cftype_neighbor, x_neighbor[nx_idx_next,:].detach()))
        else:
          data_neighbors_next.append((cftype_neighbor, x_neighbor[-1,:].detach()))

      # forward propagate
      # NOTE: here, we do not do collision checking (or updating of x_neighbors) between prop_iter for efficiency
      states_temp[i,0] = states[idx]
      for k in range(1,prop_iter+1):

        states_temp[i,k] = states_temp[i,k-1] + robot.f(torch.from_numpy(states_temp[i,k-1]), torch.from_numpy(u), data_neighbors_i).detach().numpy() * dt

      if not state_valid(robot, states_temp[i,-1], data_neighbors_next):
        continue

      # update data structures
      parents[i] = idx
      states[i] = states_temp[i,-1]
      actions[i] = u
      reward[i] = compute_reward(states[i], xf)

      if len(top_k_heap) < top_k:
        heapq.heappush(top_k_heap, (reward[i], i))
      else:
        heapq.heappushpop(top_k_heap, (reward[i], i))

      if reward[i] > best_reward:
        # print("best reward: ", reward[i])
        best_reward = reward[i]
        best_i = i
        if best_reward > -0.1:
          print("Found solution!", i, cost[i])
          best_cost = cost[i]
          cost_limit = 0.9 * cost[i]

          # generate solution
          sol_x = []
          sol_u = []
          
          idx = i
          while idx > 0:
            for k in reversed(range(1, prop_iter+1)):
              sol_x.append(states_temp[idx,k])
              sol_u.append(actions[idx])
            idx = parents[idx]
          sol_x.append(states[0])
          sol_x.reverse()
          sol_u.reverse()
          sol_x = torch.tensor(sol_x, dtype=torch.float32)
          sol_u = torch.tensor(sol_u, dtype=torch.float32)

          break

      i+=1

  return sol_x, sol_u, best_cost
