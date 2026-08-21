from framework.k8 import wait_for_pod_ready
import pytest
@pytest.mark.parametrize(
    "pod",
    [
        "open5gs-amf",
        "open5gs-smf",
        "open5gs-upf",
        "open5gs-nrf",
        "open5gs-udm",
        "open5gs-ausf",
    ],
)
def test_nf_is_ready(pod):
    assert wait_for_pod_ready(pod)
