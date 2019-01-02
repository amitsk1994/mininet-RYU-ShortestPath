from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, arp, ipv4
from ryu.lib.packet import ether_types
from ryu.lib import mac
from ryu.lib.mac import haddr_to_bin
from ryu.controller import mac_to_port
from ryu.ofproto import inet
import networkx as nx
from ryu.lib.packet import icmp
from ryu.ofproto import ether
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
from ryu.app.wsgi import ControllerBase
import array
from ryu.app.ofctl.api import get_datapath


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    global dijkstra, receive_arp, dpid_hostLookup,dijkstra_longestpath
    global path2
    path2 = [0]


    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.net = nx.DiGraph()
        self.g = nx.DiGraph()
        self.switch_map = {}

        #self.handle_arp
       # self.send_packet
       #  self.arp_table = {'10.1.0.1': '00:00:00:00:00:01',
       #                    '10.1.0.2': '00:00:00:00:00:02',
       #                    '10.1.0.3': '00:00:00:00:00:03',
       #                    '10.0.0.1': '00:00:00:00:00:11',
       #                    '10.0.0.2': '00:00:00:00:00:12',
       #                    '10.0.0.3': '00:00:00:00:00:13',
       #                    '10.0.0.4': '00:00:00:00:00:14',
       #                    '10.0.1.1': '00:00:00:00:00:21',
       #                    '10.1.1.2': '00:00:00:00:00:22',
       #                    '10.1.1.3': '00:00:00:00:00:23',
       #                    '10.1.1.4': '00:00:00:00:00:24',
       #                    '10.0.2.1': '00:00:00:00:00:31',
       #                    '10.1.2.2': '00:00:00:00:00:32',
       #                    '10.1.2.3': '00:00:00:00:00:33',
       #                    '10.1.2.4': '00:00:00:00:00:34'
       #                    }
        # self.count = 0

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        self.switch_map.update({datapath.id: datapath})

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match,inst=[],table=0):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        buffer_id = ofp.OFP_NO_BUFFER

        mod = ofp_parser.OFPFlowMod(
            datapath=datapath, table_id=table,
            command=ofp.OFPFC_ADD, priority=priority, buffer_id=buffer_id,
            out_port=ofp.OFPP_ANY, out_group=ofp.OFPG_ANY,
            match=match, instructions=inst
        )
        datapath.send_msg(mod)



    def dijkstra(graph, src, dest, visited=[], distances={}, predecessors={}):
        """ calculates a shortest path tree routed in src
        """
        # a few sanity checks
        if src not in graph:
            raise TypeError('The root of the shortest path tree cannot be found')
        if dest not in graph:
            raise TypeError('The target of the shortest path cannot be found')
            # ending condition
        if src == dest:
            # We build the shortest path and display it
            path = []
            pred = dest
            while pred != None:
                path.append(pred)
                pred = predecessors.get(pred, None)
            print('shortest path:  ' + str(path) + " cost= " + str(distances[dest]))
            global path2
            path2=path

        else:
            # if it is the initial  run, initializes the cost
            if not visited:
                distances[src] = 0
            # visit the neighbors
            for neighbor in graph[src]:
                if neighbor not in visited:
                    new_distance = distances[src] + graph[src][neighbor]
                    print(new_distance)
                    if new_distance <= distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = src
            # mark as visited
            visited.append(src)
            # now that all neighbors have been visited: recurse
            # select the non visited node with lowest distance 'x'
            # run Dijskstra with src='x'
            unvisited = {}
            for k in graph:
                if k not in visited:
                    unvisited[k] = distances.get(k, float('inf'))
            x = min(unvisited, key=unvisited.get)
            dijkstra(graph, x, dest, visited, distances, predecessors)

    def dijkstra_longestpath(graph, src, dest, visited=[], distances={}, predecessors={}):
        """ calculates a shortest path tree routed in src
        """
        # a few sanity checks
        if src not in graph:
            raise TypeError('The root of the shortest path tree cannot be found')
        if dest not in graph:
            raise TypeError('The target of the shortest path cannot be found')
            # ending condition
        if src == dest:
            # We build the shortest path and display it
            path = []
            pred = dest
            while pred != None:
                path.append(pred)
                pred = predecessors.get(pred, None)
            print('shortest path:  ' + str(path) + " cost= " + str(distances[dest]))
            global path2
            path2=path

        else:
            # if it is the initial  run, initializes the cost
            if not visited:
                distances[src] = 0
            # visit the neighbors
            for neighbor in graph[src]:
                if neighbor not in visited:
                    new_distance = distances[src] + graph[src][neighbor]
                    print(new_distance)
                    if new_distance <= distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = src
            # mark as visited
            visited.append(src)
            # now that all neighbors have been visited: recurse
            # select the non visited node with lowest distance 'x'
            # run Dijskstra with src='x'
            unvisited = {}
            for k in graph:
                if k not in visited:
                    unvisited[k] = distances.get(k, float('inf'))
            x = max(unvisited, key=unvisited.get)
            dijkstra(graph, x, dest, visited, distances, predecessors)



    def dpid_hostLookup(self, lmac):

        host_locate = {1: {'00:00:00:00:00:11', '00:00:00:00:00:12'}, 2: {'00:00:00:00:00:13', '00:00:00:00:00:14'},
                       5: {'00:00:00:00:00:21', '00:00:00:00:00:22'}, 6: {'00:00:00:00:00:23', '00:00:00:00:00:24'},
                       9: {'00:00:00:00:00:31', '00:00:00:00:00:32'}, 10: {'00:00:00:00:00:33', '00:00:00:00:00:34'},
                       13: {'00:00:00:00:00:01'}, 14: {'00:00:00:00:00:02'}, 16: {'00:00:00:00:00:03'}}
        for dpid, mac in host_locate.iteritems():
            if lmac in mac:
                return dpid



    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        pkt = packet.Packet(ev.msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        arp_pkt = pkt.get_protocol(arp.arp)
        ip4_pkt = pkt.get_protocol(ipv4.ipv4)
        if arp_pkt:
            pak = arp_pkt
        elif ip4_pkt:
            pak = ip4_pkt
        else:
            pak = eth

        self.logger.info('  _packet_in_handler: src_mac -> %s' % eth.src)
        self.logger.info('  _packet_in_handler: dst_mac -> %s' % eth.dst)
        self.logger.info('  _packet_in_handler: %s' % pak)
        self.logger.info('  ------')

        if eth.ethertype == ether_types.ETH_TYPE_LLDP or eth.ethertype == ether_types.ETH_TYPE_IPV6:
            # ignore lldp packet
            return

        dst = eth.src
        src = eth.dst
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info(">>>>>>> packet in %s %s %s %s", dpid, src, dst, in_port)
        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port
        print(src)
        print(dst)

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]


        switch_list = get_switch(self, None)
        switches = [switch.dp.id for switch in switch_list]
        links_list = get_link(self, None)
        link_port={(link.src.dpid,link.dst.dpid):link.src.port_no for link in links_list}
        # g = nx.DiGraph()
        self.g.add_nodes_from(switches)
        links = [(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
        print(links)
        self.g.add_edges_from(links)
        links = [(link.dst.dpid,link.src.dpid,{'port':link.dst.port_no})  for link in links_list]
        self.g.add_edges_from(links)
        #print(links)
        #print(self.g)

        topo = {'1': {'3': 50, '4': 100}, '2': {'3': 100, '4': 50}, '3': {'1': 50, '2': 100, '13': 15, '14': 100},
                '4': {'1': 100, '2': 50, '14': 5}, '5': {'7': 50, '8': 100}, '6': {'7': 100, '8': 50},
                '7': {'5': 50, '6': 100, '13': 15, '14': 20, '15': 5}, '8': {'5': 100, '6': 50, '15': 10, '16': 15},
                '9': {'11': 50, '12': 100}, '10': {'11': 100, '12': 50},
                '11': {'9': 50, '10': 100, '14': 10}, '12': {'9': 100, '10': 50, '15': 15, '16': 10},
                '13': {'3': 15, '7': 15}, '14': {'3': 10, '4': 5, '7': 20, '11': 10}, '15': {'7': 5, '8': 10, '12': 15},
                '16': {'8': 15, '12': 10}}

        dst_dpid = dpid_hostLookup(self, dst)
        print("dpid",str(dpid))
        print("dst",dst)
        # if(dst=='ff:ff:ff:ff:ff:ff'):
        #     return()
        path3=[]
        src=str(src)
        dst=str(dst)
        print("dst dpid",str(dst_dpid))
        if ((src == '00:00:00:00:00:01' and dst == '00:00:00:00:00:13') or (src == '00:00:00:00:00:01' and dst == '00:00:00:00:00:23') or (
            src == '00:00:00:00:00:01' and dst == '00:00:00:00:00:33') or(src == '00:00:00:00:00:02' and dst == '00:00:00:00:00:12') or (
            src == '00:00:00:00:00:02' and dst == '00:00:00:00:00:22') or (src == '00:00:00:00:00:02' and dst == '00:00:00:00:00:32') or
            (src == '00:00:00:00:00:03' and dst == '00:00:00:00:00:14') or (src == '00:00:00:00:00:03' and dst == '00:00:00:00:00:24') or (
                        src == '00:00:00:00:00:03' and dst == '00:00:00:00:00:34')):
         dijkstra(topo, str(dpid), str(dst_dpid))
         global path2
         path3= list(map(int, path2))
         print(path3)
         path3.reverse()

        elif ((src == '00:00:00:00:00:01' and (dst == '00:00:00:00:00:11' or dst == '00:00:00:00:00:12' or dst == '00:00:00:00:00:14' or dst == '00:00:00:00:00:21' or dst == '00:00:00:00:00:22' or dst == '00:00:00:00:00:24' or dst == '00:00:00:00:00:31' or dst == '00:00:00:00:00:32' or dst == '00:00:00:00:00:34'))
              or (src == '00:00:00:00:00:02' and (dst == '00:00:00:00:00:11' or dst == '00:00:00:00:00:13' or dst == '00:00:00:00:00:14' or dst == '00:00:00:00:00:21' or dst == '00:00:00:00:00:23' or dst == '00:00:00:00:00:24' or dst == '00:00:00:00:00:31' or dst == '00:00:00:00:00:33' or dst == '00:00:00:00:00:34'))
              or (src == '00:00:00:00:00:03' and (dst == '00:00:00:00:00:11' or dst == '00:00:00:00:00:12' or dst == '00:00:00:00:00:13' or dst == '00:00:00:00:00:21' or dst == '00:00:00:00:00:22' or dst == '00:00:00:00:00:23' or dst == '00:00:00:00:00:31' or dst == '00:00:00:00:00:32' or dst == '00:00:00:00:00:33'))):
            dijkstra_longestpath(topo, str(dpid), str(dst_dpid))
            path3 = list(map(int, path2))
            print(path3)
            path3.reverse()


        if not self.g.has_node(eth.src):
            print("add %s in self.net" % eth.src)
            self.g.add_node(eth.src)
            self.g.add_edge(eth.src, datapath.id)
            self.g.add_edge(datapath.id, eth.src, {'port': in_port})
            print(self.g.node)

        if not self.g.has_node(eth.dst):
            print("add %s in self.net" % eth.dst)
            self.g.add_node(eth.dst)
            self.g.add_edge(eth.dst, datapath.id)
            self.g.add_edge(datapath.id, eth.dst, {'port': in_port})
            print(self.g.node)

       # path3=[13,3,1]
        print("before loop")
        if(path3!=[]):
         if self.g.has_node(eth.dst):
            next_match = parser.OFPMatch(eth_dst=eth.dst)
            back_match = parser.OFPMatch(eth_dst=eth.src)
            print(path3)
            for on_path_switch in range(1, len(path3) - 1):
                print("hi in loop")
                now_switch = path3[on_path_switch]
                next_switch = path3[on_path_switch + 1]
                back_switch = path3[on_path_switch - 1]
                next_port = link_port[(now_switch,next_switch)]
                back_port = link_port[(now_switch,back_switch)]
                print("next_port",next_port)
                print("back_port",back_port)
                new_dp=get_datapath(self, next_switch)
                action = parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                          [parser.OFPActionOutput(next_port)])
                inst = [action]
                self.add_flow(datapath=new_dp, match=next_match, inst=inst, table=0)

                action = parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                          [parser.OFPActionOutput(back_port)])
                inst = [action]
                actions = [parser.OFPActionOutput(next_port)]
                new_dp = get_datapath(self, back_switch)
                self.add_flow(datapath=new_dp, match=back_match, inst=inst,actions=action, table=0)
                print ("now switch:%s",now_switch)
                out = datapath.ofproto_parser.OFPPacketOut(
                    datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
                    actions=actions)
                datapath.send_msg(out)
                print("final")

            else:
                return
        else:
            if out_port != ofproto.OFPP_FLOOD:
                self.add_flow(datapath, msg.in_port, dst, actions)

            out = datapath.ofproto_parser.OFPPacketOut(
                datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
                actions=actions)
            datapath.send_msg(out)



