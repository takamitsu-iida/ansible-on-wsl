Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).




show bgp neighbors
------------------


```text
RP/0/RP0/CPU0:R5-core#show bgp neighbors
Mon Jun 14 18:32:34.542 JST

BGP neighbor is 10.255.255.1
 Remote AS 65452, local AS 65452, internal link
 Remote router ID 10.255.255.1
 Cluster ID 65452
  BGP state = Established, up for 1d21h
  NSR State: None
  BFD enabled (session down, BFD not configured on remote neighbor)
  Last read 00:00:16, Last read before reset 00:00:00
  Hold time is 180, keepalive interval is 60 seconds
  Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
  Last write 00:00:23, attempted 19, written 19
  Second last write 00:01:23, attempted 19, written 19
  Last write before reset 00:00:00, attempted 0, written 0
  Second last write before reset 00:00:00, attempted 0, written 0
  Last write pulse rcvd  Jun 14 18:32:18.444 last full not set pulse count 5343
  Last write pulse rcvd before reset 00:00:00
  Socket not armed for io, armed for read, armed for write
  Last write thread event before reset 00:00:00, second last 00:00:00
  Last KA expiry before reset 00:00:00, second last 00:00:00
  Last KA error before reset 00:00:00, KA not sent 00:00:00
  Last KA start before reset 00:00:00, second last 00:00:00
  Precedence: internet
  Non-stop routing is enabled
  Multi-protocol capability received
  Neighbor capabilities:
    Route refresh: advertised (old + new) and received (old + new)
    4-byte AS: advertised and received
    Address family IPv4 Unicast: advertised and received
    Address family VPNv4 Unicast: advertised and received
    Address family L2VPN EVPN: advertised and received
  Received 2713 messages, 0 notifications, 0 in queue
  Sent 2716 messages, 0 notifications, 0 in queue
  Minimum time between advertisement runs is 0 secs
  Inbound message logging enabled, 3 messages buffered
  Outbound message logging enabled, 3 messages buffered

 For Address Family: IPv4 Unicast
  BGP neighbor version 11
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 11, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes
  Advertise routes with local-label via Unicast SAFI

 For Address Family: VPNv4 Unicast
  BGP neighbor version 1
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 1, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

 For Address Family: L2VPN EVPN
  BGP neighbor version 5
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
  Route refresh request: received 0, sent 0
  1 accepted prefixes, 1 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 4, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was not received during read-only mode
  Last ack version 5, Last synced ack version 0
  Outstanding version objects: current 0, max 1, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

  Connections established 1; dropped 0
  Local host: 10.255.255.5, Local port: 179, IF Handle: 0x00000000
  Foreign host: 10.255.255.1, Foreign port: 26981
  Last reset 00:00:00

BGP neighbor is 10.255.255.2
 Remote AS 65452, local AS 65452, internal link
 Remote router ID 10.255.255.2
 Cluster ID 65452
  BGP state = Established, up for 1d21h
  NSR State: None
  BFD enabled (session down, BFD not configured on remote neighbor)
  Last read 00:00:45, Last read before reset 00:00:00
  Hold time is 180, keepalive interval is 60 seconds
  Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
  Last write 00:00:23, attempted 19, written 19
  Second last write 00:01:23, attempted 19, written 19
  Last write before reset 00:00:00, attempted 0, written 0
  Second last write before reset 00:00:00, attempted 0, written 0
  Last write pulse rcvd  Jun 14 18:32:11.485 last full not set pulse count 5422
  Last write pulse rcvd before reset 00:00:00
  Socket not armed for io, armed for read, armed for write
  Last write thread event before reset 00:00:00, second last 00:00:00
  Last KA expiry before reset 00:00:00, second last 00:00:00
  Last KA error before reset 00:00:00, KA not sent 00:00:00
  Last KA start before reset 00:00:00, second last 00:00:00
  Precedence: internet
  Non-stop routing is enabled
  Multi-protocol capability received
  Neighbor capabilities:
    Route refresh: advertised (old + new) and received (old + new)
    4-byte AS: advertised and received
    Address family IPv4 Unicast: advertised and received
    Address family VPNv4 Unicast: advertised and received
    Address family L2VPN EVPN: advertised and received
  Received 2713 messages, 0 notifications, 0 in queue
  Sent 2717 messages, 0 notifications, 0 in queue
  Minimum time between advertisement runs is 0 secs
  Inbound message logging enabled, 3 messages buffered
  Outbound message logging enabled, 3 messages buffered

 For Address Family: IPv4 Unicast
  BGP neighbor version 11
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 11, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes
  Advertise routes with local-label via Unicast SAFI

 For Address Family: VPNv4 Unicast
  BGP neighbor version 1
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 1, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

 For Address Family: L2VPN EVPN
  BGP neighbor version 5
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
  Route refresh request: received 0, sent 0
  1 accepted prefixes, 1 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 4, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 5, Last synced ack version 0
  Outstanding version objects: current 0, max 1, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

  Connections established 1; dropped 0
  Local host: 10.255.255.5, Local port: 179, IF Handle: 0x00000000
  Foreign host: 10.255.255.2, Foreign port: 31831
  Last reset 00:00:00

BGP neighbor is 10.255.255.3
 Remote AS 65452, local AS 65452, internal link
 Remote router ID 10.255.255.3
 Cluster ID 65452
  BGP state = Established, up for 1d21h
  NSR State: None
  BFD enabled (session down, BFD not configured on remote neighbor)
  Last read 00:00:11, Last read before reset 00:00:00
  Hold time is 180, keepalive interval is 60 seconds
  Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
  Last write 00:00:23, attempted 19, written 19
  Second last write 00:01:23, attempted 19, written 19
  Last write before reset 00:00:00, attempted 0, written 0
  Second last write before reset 00:00:00, attempted 0, written 0
  Last write pulse rcvd  Jun 14 18:32:23.357 last full not set pulse count 5404
  Last write pulse rcvd before reset 00:00:00
  Socket not armed for io, armed for read, armed for write
  Last write thread event before reset 00:00:00, second last 00:00:00
  Last KA expiry before reset 00:00:00, second last 00:00:00
  Last KA error before reset 00:00:00, KA not sent 00:00:00
  Last KA start before reset 00:00:00, second last 00:00:00
  Precedence: internet
  Non-stop routing is enabled
  Multi-protocol capability received
  Neighbor capabilities:
    Route refresh: advertised (old + new) and received (old + new)
    4-byte AS: advertised and received
    Address family IPv4 Unicast: advertised and received
    Address family VPNv4 Unicast: advertised and received
    Address family L2VPN EVPN: advertised and received
  Received 2713 messages, 0 notifications, 0 in queue
  Sent 2716 messages, 0 notifications, 0 in queue
  Minimum time between advertisement runs is 0 secs
  Inbound message logging enabled, 3 messages buffered
  Outbound message logging enabled, 3 messages buffered

 For Address Family: IPv4 Unicast
  BGP neighbor version 11
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 11, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes
  Advertise routes with local-label via Unicast SAFI

 For Address Family: VPNv4 Unicast
  BGP neighbor version 1
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 1, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

 For Address Family: L2VPN EVPN
  BGP neighbor version 5
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
  Route refresh request: received 0, sent 0
  1 accepted prefixes, 1 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 4, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was not received during read-only mode
  Last ack version 5, Last synced ack version 0
  Outstanding version objects: current 0, max 1, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

  Connections established 1; dropped 0
  Local host: 10.255.255.5, Local port: 36353, IF Handle: 0x00000000
  Foreign host: 10.255.255.3, Foreign port: 179
  Last reset 00:00:00

BGP neighbor is 10.255.255.4
 Remote AS 65452, local AS 65452, internal link
 Remote router ID 10.255.255.4
 Cluster ID 65452
  BGP state = Established, up for 1d21h
  NSR State: None
  BFD enabled (session down, BFD not configured on remote neighbor)
  Last read 00:00:24, Last read before reset 00:00:00
  Hold time is 180, keepalive interval is 60 seconds
  Configured hold time: 180, keepalive: 60, min acceptable hold time: 3
  Last write 00:00:23, attempted 19, written 19
  Second last write 00:01:23, attempted 19, written 19
  Last write before reset 00:00:00, attempted 0, written 0
  Second last write before reset 00:00:00, attempted 0, written 0
  Last write pulse rcvd  Jun 14 18:32:11.484 last full not set pulse count 5424
  Last write pulse rcvd before reset 00:00:00
  Socket not armed for io, armed for read, armed for write
  Last write thread event before reset 00:00:00, second last 00:00:00
  Last KA expiry before reset 00:00:00, second last 00:00:00
  Last KA error before reset 00:00:00, KA not sent 00:00:00
  Last KA start before reset 00:00:00, second last 00:00:00
  Precedence: internet
  Non-stop routing is enabled
  Multi-protocol capability received
  Neighbor capabilities:
    Route refresh: advertised (old + new) and received (old + new)
    4-byte AS: advertised and received
    Address family IPv4 Unicast: advertised and received
    Address family VPNv4 Unicast: advertised and received
    Address family L2VPN EVPN: advertised and received
  Received 2713 messages, 0 notifications, 0 in queue
  Sent 2716 messages, 0 notifications, 0 in queue
  Minimum time between advertisement runs is 0 secs
  Inbound message logging enabled, 3 messages buffered
  Outbound message logging enabled, 3 messages buffered

 For Address Family: IPv4 Unicast
  BGP neighbor version 11
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 11, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes
  Advertise routes with local-label via Unicast SAFI

 For Address Family: VPNv4 Unicast
  BGP neighbor version 1
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
    Extended Nexthop Encoding: advertised and received
  Route refresh request: received 0, sent 0
  0 accepted prefixes, 0 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 0, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was received during read-only mode
  Last ack version 1, Last synced ack version 0
  Outstanding version objects: current 0, max 0, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

 For Address Family: L2VPN EVPN
  BGP neighbor version 5
  Update group: 0.2 Filter-group: 0.1  No Refresh request being processed
  Route-Reflector Client
  Route refresh request: received 0, sent 0
  1 accepted prefixes, 1 are bestpaths
  Exact no. of prefixes denied : 0.
  Cumulative no. of prefixes denied: 0.
  Prefix advertised 4, suppressed 0, withdrawn 0
  AIGP is enabled
  An EoR was not received during read-only mode
  Last ack version 5, Last synced ack version 0
  Outstanding version objects: current 0, max 1, refresh 0
  Additional-paths operation: None
  Send Multicast Attributes

  Connections established 1; dropped 0
  Local host: 10.255.255.5, Local port: 179, IF Handle: 0x00000000
  Foreign host: 10.255.255.4, Foreign port: 47014
  Last reset 00:00:00
RP/0/RP0/CPU0:R5-core#

```