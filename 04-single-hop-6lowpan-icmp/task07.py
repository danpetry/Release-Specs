#! /usr/bin/env python3
# Copyright (C) 2018 Freie Universität Berlin
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

import sys
import os

COUNT           = 1000
PAYLOAD_SIZE    = 50
DELAY           = 100   # ms
CHANNEL         = 17
ERROR_TOLERANCE = 10    # %


def task07(riotbase, runs=1):
    os.chdir(os.path.join(riotbase, "examples/gnrc_networking"))
    try:
        exp = IoTLABExperiment("RIOT-release-test-04-07",
                               [IoTLABNode("samr21-xpro", "saclay",
                                           ["gnrc_pktbuf_cmd"]),
                                IoTLABNode("arduino-zero", "saclay",
                                           ["gnrc_pktbuf_cmd", "xbee"])])
    except Exception as e:
        print(str(e))
        print("Can't start experiment")
        return

    try:
        nodes = exp.nodes
        iotlab_cmd = "make IOTLAB_NODE={} BOARD={} term"
        source = SixLoWPANNode(iotlab_cmd.format(nodes[0].addr, nodes[0].board))
        dest = SixLoWPANNode(iotlab_cmd.format(nodes[1].addr, nodes[1].board))
        results = []

        for run in range(runs):
            print("Run {}/{}: ".format(run + 1, runs), end="")
            packet_loss, buf_source, buf_dest = ping(source, dest, "ff02::1",
                                                     COUNT, PAYLOAD_SIZE, DELAY,
                                                     CHANNEL)
            results.append([packet_loss, buf_source, buf_dest])
            packet_loss, buf_source, buf_dest = ping(dest, source, "ff02::1",
                                                     COUNT, PAYLOAD_SIZE, DELAY,
                                                     CHANNEL)
            results.append([packet_loss, buf_source, buf_dest])

            assert(packet_loss < ERROR_TOLERANCE)
            assert(buf_source)
            assert(buf_dest)
            print("OK")
        print_results(results)
    except Exception as e:
        print("FAILED")
        print(str(e))
    finally:
        exp.stop()


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "../", "testutils"))
    from iotlab import IoTLABNode, IoTLABExperiment
    from common import argparser, SixLoWPANNode, ping, print_results

    args = argparser.parse_args()
    task07(**vars(args))