#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
from mpi4py import MPI

<<<<<<< HEAD:stable_baselines/trpo_mpi/run_mujoco.py
from stable_baselines.common.cmd_util import make_mujoco_env, mujoco_arg_parser
from stable_baselines import logger
from stable_baselines.ppo1.mlp_policy import MlpPolicy
from stable_baselines.trpo_mpi import trpo_mpi
import stable_baselines.common.tf_util as tf_util
=======
from baselines.common.cmd_util import make_mujoco_env, mujoco_arg_parser
from baselines import logger
from baselines.ppo1.mlp_policy import MlpPolicy
from baselines.trpo_mpi import TRPO
import baselines.common.tf_util as tf_util
>>>>>>> refactoring:baselines/trpo_mpi/run_mujoco.py


def train(env_id, num_timesteps, seed):
    """
    Train TRPO model for the mujoco environment, for testing purposes

    :param env_id: (str) Environment ID
    :param num_timesteps: (int) The total number of samples
    :param seed: (int) The initial seed for training
    """
    with tf_util.single_threaded_session():
        rank = MPI.COMM_WORLD.Get_rank()
        if rank == 0:
            logger.configure()
        else:
            logger.configure(format_strs=[])
            logger.set_level(logger.DISABLED)
        workerseed = seed + 10000 * MPI.COMM_WORLD.Get_rank()

        def policy_fn(name, ob_space, ac_space, sess=None, placeholders=None):
            return MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space, hid_size=32, num_hid_layers=2, sess=sess,
                             placeholders=placeholders)

        env = make_mujoco_env(env_id, workerseed)
        model = TRPO(policy_fn, env, timesteps_per_batch=1024, max_kl=0.01, cg_iters=10, cg_damping=0.1, entcoeff=0.0,
                     gamma=0.99, lam=0.98, vf_iters=5, vf_stepsize=1e-3)
        model.learn(total_timesteps=num_timesteps)
        env.close()


def main():
    """
    Runs the test
    """
    args = mujoco_arg_parser().parse_args()
    train(args.env, num_timesteps=args.num_timesteps, seed=args.seed)


if __name__ == '__main__':
    main()