import logging
import torch.distributed as dist
import os


class ProcessGroupManager:

    def __init__(self, rank, world_size, master_address, master_port, only_gpu):
        logging.info("Start process group")

        env_dict = {
            key: os.environ[key]
            for key in ("MASTER_ADDR", "MASTER_PORT", "RANK", "WORLD_SIZE")
        }
        logging.info(
            f"[{os.getpid()}] Initializing process group with: {env_dict}")
        backend = dist.Backend.NCCL if only_gpu else dist.Backend.GLOO
        # initialize the process group
        dist.init_process_group(
            backend=backend)
        self.messaging_pg = dist.new_group()
        # dist.init_process_group()

        logging.info("Initiated")

    def cleanup(self):
        dist.destroy_process_group()

    def get_process_group(self):
        return self.messaging_pg
