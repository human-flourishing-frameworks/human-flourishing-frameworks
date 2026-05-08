import hmac
import hashlib
import json

class CryptographicProof:
    def __init__(self, secret_key='default-secret-key'):
        self.secret_key = secret_key
    
    def sign_violation(self, violation_data):
        canonical = json.dumps(violation_data, sort_keys=True)
        signature = hmac.new(
            self.secret_key.encode(),
            canonical.encode(),
            hashlib.sha256
        ).hexdigest()
        data_hash = hashlib.sha256(canonical.encode()).hexdigest()
        
        return {
            **violation_data,
            'signature': signature,
            'hash': data_hash,
            'algorithm': 'HMAC-SHA256'
        }
    
    def verify_signature(self, signed_data):
        signature = signed_data.pop('signature', None)
        canonical = json.dumps(signed_data, sort_keys=True)
        expected_sig = hmac.new(
            self.secret_key.encode(),
            canonical.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature == expected_sig
    
    def sign_proposal(self, proposal_data):
        return self.sign_violation(proposal_data)
    
    def create_merkle_root(self, records):
        hashes = [r.get('hash', '') for r in records]
        while len(hashes) > 1:
            if len(hashes) % 2:
                hashes.append(hashes[-1])
            hashes = [hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest()
                     for i in range(0, len(hashes), 2)]
        return hashes[0] if hashes else ''