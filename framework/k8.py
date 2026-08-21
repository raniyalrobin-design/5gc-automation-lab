import json
import subprocess
import time
from framework.logger import get_logger
logger = get_logger(__name__)


def run_kubectl(args):
    """Run a kubectl command and return stdout."""
    result = subprocess.run(
        ["kubectl"] + args,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_nodes():
    """Return Kubernetes nodes as a Python dictionary."""
    output = run_kubectl(
        ["get", "nodes", "-o", "json"]
    )
    return json.loads(output)


def get_open5gs_pods():
    """Return Open5GS pods as a Python dictionary."""
    output = run_kubectl(
        [
            "get",
            "pods",
            "-n",
            "open5gs",
            "-o",
            "json",
        ]
    )
    return json.loads(output)


def wait_for_pod_ready(pod_name, timeout=10, interval=5):
    """Wait until a pod becomes Ready."""

    start_time = time.time()

    while time.time() - start_time < timeout:

        pods = get_open5gs_pods()

        pod_found = False

        for pod in pods["items"]:

            name = pod["metadata"]["name"]

            if name.startswith(pod_name):

                pod_found = True

                container_statuses = pod["status"].get(
                    "containerStatuses", []
                )

                if len(container_statuses) > 0:

                    all_ready = True

                    for container in container_statuses:

                        if container["ready"] == False:
                            all_ready = False

                            logger.warning(
                                f"Container {container['name']} "
                                f"is not ready"
                            )

                            logger.info(
                                f"Restart count: "
                                f"{container.get('restartCount', 0)}"
                            )

                            last_state = container.get(
                                "lastState", {}
                            )

                            logger.info(
                                f"Last state: {last_state}"
                            )

                    if all_ready:
                        logger.info(f"Pod {name} is ready")
                        return True

                logger.warning(
                    f"Pod {name} is not ready. "
                    f"Retrying in {interval} seconds..."
                )

                break

        if pod_found == False:
            logger.warning(
                f"Pod starting with '{pod_name}' "
                f"was not found. "
                f"Retrying in {interval} seconds..."
            )

        time.sleep(interval)

    logger.error(
        f"Pod '{pod_name}' did not become ready "
        f"within {timeout} seconds."
    )

    return False
