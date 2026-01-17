"""Module to run functions in parallel processes with retry logic."""

__all__ = ["run_in_parallel", "log_process_details"]


import multiprocessing
from src.common.base_logger import log

MAX_RETRIES = 3


def log_process_details(arg, retry_cnt):
    """Logs the process details including parent and child process IDs, argument, and retry count."""
    import os

    print(
        f"parent: {os.getppid()}, "
        f"child process: {os.getpid()} "
        f"Argument: {arg}, "
        f"retry count: {retry_cnt}"
    )

    if arg == "fail":
        raise Exception("Simulated exception in child process")


def run_in_parallel(args_list, func):
    """Runs the given function in parallel processes for each argument in args_list."""
    retry_state = {arg: 0 for arg in args_list}
    args_to_run = set(args_list)

    while args_to_run:
        processes = {}
        for arg in args_to_run:
            p = multiprocessing.Process(
                target=func, kwargs={"arg": arg, "retry_cnt": retry_state[arg]}
            )
            processes[arg] = p
            p.start()
        for arg, p in processes.items():
            p.join()

        failed_args = set()
        for arg, p in processes.items():
            if p.exitcode != 0:
                log.error(
                    f"Process {p.pid} for arg {arg} failed with exit code {p.exitcode}"
                )
                retry_state[arg] += 1
                print(retry_state)
                if retry_state[arg] < MAX_RETRIES:
                    failed_args.add(arg)
                else:
                    log.error(f"Arg {arg} reached max retries ({MAX_RETRIES})")
                    exit(1)
        args_to_run = failed_args


if __name__ == "__main__":
    # Example usage with list of strings
    run_in_parallel(["a", "b", "fail", "d"], log_process_details)
