from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, BaseResolver
from pathlib import Path

class SinkholeResolver(BaseResolver):
    def __init__(self, blacklist_path):
        self.blacklist = self.load_blacklist(blacklist_path)
        print(f"[✓] {len(self.blacklist)} domain blacklist dimuat.")

    def load_blacklist(self, path):
        with open(path, "r") as f:
            return set(line.strip().lower() for line in f if line.strip())

    def resolve(self, request, handler):
        qname = str(request.q.qname).strip('.')
        if qname.lower() in self.blacklist:
            print(f"[BLOCKED] {qname}")
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A("0.0.0.0"), ttl=60))
            return reply
        else:
            try:
                proxy_req = DNSRecord.question(qname)
                response = proxy_req.send("8.8.8.8", 53, timeout=2)
                return DNSRecord.parse(response)
            except Exception as e:
                print(f"[!] Error resolving {qname}: {e}")
                return request.reply()

def start_dns_server(blacklist_path, port=5353):
    resolver = SinkholeResolver(blacklist_path)
    server = DNSServer(resolver, port=port, address="0.0.0.0")
    server.start_thread()
    print(f"[✓] DNS server berjalan di port {port}...")
    return server
