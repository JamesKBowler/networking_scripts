proc WakeOnLan {broadcastAddr macAddr} {
     set net [binary format H* [join [split $macAddr -:] ""]]
     set pkt [binary format c* {0xff 0xff 0xff 0xff 0xff 0xff}]

     for {set i 0} {$i < 16} {incr i} {
        append pkt $net
     }

     # Open UDP and Send the Magic Paket.
     set udpSock [udp_open]
     fconfigure $udpSock -translation binary \
          -remote [list $broadcastAddr 4580] \
          -broadcast 1
     puts $udpSock $pkt
     flush $udpSock;
     close $udpSock
}

WakeOnLan 255.255.255.255 74d435ABC123
