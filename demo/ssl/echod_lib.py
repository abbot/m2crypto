#!/usr/bin/env python

"""Support routines for the various SSL 'echo' servers.

Copyright (c) 1999-2000 Ng Pheng Siong. All rights reserved."""

RCS_id='$Id: echod_lib.py,v 1.2 2000/04/17 15:58:15 ngps Exp $'

import SocketServer
from M2Crypto import Err, SSL

def init_context(protocol, certfile, cafile, verify, verify_depth=10):
    ctx=SSL.Context(protocol)
    ctx.load_cert(certfile)
    ctx.load_client_ca(cafile)
    ctx.load_verify_info(cafile)
    ctx.set_verify(verify, verify_depth)
    ctx.set_allow_unknown_ca(1)
    ctx.set_session_id_ctx('echod')
    ctx.set_info_callback()
    return ctx


class ssl_echo_handler(SocketServer.BaseRequestHandler):

    buffer='Ye Olde Echo Servre\r\n'

    def handle(self):
        if not self.request.verify_ok():
            v = self.request.get_verify_result()
            print 'peer verification failed:', Err.get_x509_verify_error(v)
            return
        peer = self.request.get_peer_cert()
        if peer is not None:
            print 'Client CA        =', peer.get_issuer().O
            print 'Client Subject   =', peer.get_subject()
        self.request.write(self.buffer)
        while 1:
            try:
                buf = self.request.read()
                if not buf:
                    break
                self.request.write(buf) 
            except:
                break

    def finish(self):
        self.request.close()
