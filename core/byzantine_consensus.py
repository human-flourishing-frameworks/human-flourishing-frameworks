import sqlite3
import json
from datetime import datetime

class ByzantineConsensus:
    def __init__(self, db_path='consensus.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS proposals
                     (id TEXT PRIMARY KEY, data TEXT, created_at TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS votes
                     (proposal_id TEXT, voter_id TEXT, vote TEXT, timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS statistics
                     (metric TEXT, value TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()
    
    def propose_violation(self, violation_data):
        import uuid
        proposal_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO proposals VALUES (?, ?, ?)',
                  (proposal_id, json.dumps(violation_data), datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        return proposal_id
    
    def cast_vote(self, proposal_id, vote):
        import uuid
        voter_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO votes VALUES (?, ?, ?, ?)',
                  (proposal_id, voter_id, vote, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        return voter_id
    
    def tally_votes(self, proposal_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT vote FROM votes WHERE proposal_id = ?', (proposal_id,))
        votes = c.fetchall()
        conn.close()
        
        if not votes:
            return {'consensus_reached': False, 'approved': False}
        
        votes_for = sum(1 for v in votes if v[0] == 'yes')
        total = len(votes)
        threshold = (total * 2) // 3 + 1
        
        return {
            'votes_for': votes_for,
            'total': total,
            'threshold': threshold,
            'approved': votes_for >= threshold,
            'consensus_reached': votes_for >= threshold or (total - votes_for) > total - threshold
        }
    
    def get_pending_proposals(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT id, data FROM proposals')
        rows = c.fetchall()
        conn.close()
        return [{'id': r[0], 'data': json.loads(r[1])} for r in rows]
    
    def propose_protocol_change(self, changes):
        return self.propose_violation({'type': 'protocol_change', 'changes': changes})
    
    def get_statistics(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM proposals')
        proposal_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM votes')
        vote_count = c.fetchone()[0]
        conn.close()
        return {'proposal_count': proposal_count, 'vote_count': vote_count, 'peer_count': 3}