#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import argparse
import socket
import struct


class WakeOnLan:
    _broadcast_ip = '255.255.255.255'
    _port = 7

    def __init__(self, ip = '255.255.255.255', port = 7):
        self._port = port
        self._broadcast_ip = ip

    def create_magic_packet(self, mac):
        """
        创建magic packet
        Args:
            mac (str): 网卡MAC地址.
        """
        if len(mac) == 12:
            pass
        elif len(mac) == 17:
            # 去除地址中的-或者:
            sep = mac[2]
            mac = mac.replace(sep, '')
        else:
            raise ValueError('网卡地址不正确')
        # Pad the synchronization stream.
        data = b'FFFFFFFFFFFF' + (mac * 16).encode()
        send_data = b''
        """
        WOL包结构：
        Synchronization Stream | MAC地址块 | Password (optional)
                6                   96              0, 4 或 6
        The Synchronization Stream is defined as 6 bytes of FFh.
        目标MAC地址块 包含16个重复的IEEE目标地址，不含空格或者隔断
        Password是可选的，如果包含，则长度为4或6字节。如果是4字节，则解析为ipv4地址，如果未6字节，则解析为MAC地址。
        """
        for i in range(0, len(data), 2):
            send_data += struct.pack(b'B', int(data[i: i + 2], 16))
        return send_data

    def send_magic_packet(self, macs):
        """
        向指定网卡发送magic packet
        Args:
            macs (str): One or more macaddresses of machines to wake.
        """
        packets = []

        for mac in macs:
            packet = self.create_magic_packet(mac)
            packets.append(packet)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.connect((self._broadcast_ip, self._port))
        for packet in packets:
            sock.send(packet)
        sock.close()
