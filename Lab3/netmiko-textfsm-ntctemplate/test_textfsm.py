"""
    TDD: correctness of textfsmlab.py, referring to the network topology.
"""

import pytest
import textfsmlab

CDP_R1 = """Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
S1               Gig 0/1           150             S I     WS-C2960  Gig 0/1
R2               Gig 0/2           155              R B     CSR1000V Gig 0/1

Total cdp entries displayed : 2
"""

CDP_R2 = """Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R1               Gig 0/1           150              R B     CSR1000V Gig 0/2

Total cdp entries displayed : 1
"""

CDP_S1 = """Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R1               Gig 0/1           150              R B     CSR1000V Gig 0/1

Total cdp entries displayed : 1
"""


@pytest.fixture
def setup_teardown():
    print("Setup Test")
    yield
    print("Clean Test")


@pytest.mark.parametrize("raw,expected", [
    ("Gig 0/2", "G0/2"),
    ("GigabitEthernet0/1", "G0/1"),
    ("Gi0/3", "G0/3"),
    ("g0/1", "G0/1"),
    ("FastEthernet0/0", "F0/0"),
])
def test_short_interface(raw, expected):
    assert textfsmlab.short_interface(raw) == expected

def test_parse_cdp_neighbors_extracts_fields():
    parsed = textfsmlab.parse_cdp_neighbors(CDP_R1)
    assert {(n["local_interface"], n["neighbor_name"], n["neighbor_interface"])
            for n in parsed} == {
        ("Gig 0/1", "S1", "Gig 0/1"),
        ("Gig 0/2", "R2", "Gig 0/1"),
    }

def test_r1_g0_2_connects_to_r2():
    """Assignment example: G0/2 of R1 -> "Connect to G0/1 of R2"."""
    desc = textfsmlab.interface_descriptions(CDP_R1, ["g0/1", "g0/2"])
    assert desc["G0/2"] == "Connect to G0/1 of R2"

def test_r1_descriptions():
    desc = textfsmlab.interface_descriptions(CDP_R1, ["g0/1", "g0/2"])
    assert desc == {
        "G0/1": "Connect to G0/1 of S1",
        "G0/2": "Connect to G0/1 of R2",
    }

def test_r2_descriptions():
    desc = textfsmlab.interface_descriptions(
        CDP_R2, ["g0/1", "g0/2", "g0/3"], wan_interfaces=["g0/3"]
    )
    assert desc == {
        "G0/1": "Connect to G0/2 of R1",
        "G0/2": "Connect to PC",
        "G0/3": "Connect to WAN",
    }

def test_r2_g0_3_is_wan():
    desc = textfsmlab.interface_descriptions(
        CDP_R2, ["g0/1", "g0/2", "g0/3"], wan_interfaces=["g0/3"]
    )
    assert desc["G0/3"] == "Connect to WAN"

def test_r2_g0_2_is_pc():
    desc = textfsmlab.interface_descriptions(
        CDP_R2, ["g0/1", "g0/2", "g0/3"], wan_interfaces=["g0/3"]
    )
    assert desc["G0/2"] == "Connect to PC"

def test_s1_descriptions():
    desc = textfsmlab.interface_descriptions(CDP_S1, ["g0/1", "g0/2"])
    assert desc == {
        "G0/1": "Connect to G0/1 of R1",
        "G0/2": "Connect to PC",
    }
