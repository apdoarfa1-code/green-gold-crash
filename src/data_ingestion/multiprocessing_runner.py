import multiprocessing
import time
from config.logging_config import logger


def worker_process_target(worker_id: int, queue: multiprocessing.Queue):
    """Isolated worker process for decentralized scraping tasks."""
    logger.info(f"Ingestion Worker {worker_id} started (PID: {multiprocessing.current_process().pid})")
    try:
        while True:
            # Simulated data collection pulse
            time.sleep(5)
            sample_data = {
                "worker_id": worker_id,
                "round_id": f"rnd_{int(time.time())}_{worker_id}",
                "multiplier": round(1.0 + (worker_id * 0.1), 2),
                "timestamp": time.time()
            }
            queue.put(sample_data)
    except KeyboardInterrupt:
        logger.info(f"Worker {worker_id} terminated.")


class MultiprocessingCollectorPool:
    """Manages pool of parallel ingestion workers."""

    def __init__(self, num_workers: int = 2):
        self.num_workers = num_workers
        self.queue = multiprocessing.Queue()
        self.workers = []

    def start(self):
        logger.info(f"Starting ingestion pool with {self.num_workers} workers...")
        for i in range(self.num_workers):
            p = multiprocessing.Process(target=worker_process_target, args=(i, self.queue))
            p.daemon = True
            p.start()
            self.workers.append(p)

    def get_data(self, timeout: float = 1.0):
        try:
            return self.queue.get(timeout=timeout)
        except Exception:
            return None

    def stop(self):
        for p in self.workers:
            if p.is_alive():
                p.terminate()
                p.join()
        logger.info("All ingestion workers stopped.")
