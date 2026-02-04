import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
LOG_FILE = "verify_result.txt"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def wait_for_api():
    log("⏳ Waiting for API to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                log("✅ API is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
    log("❌ API failed to start in time.")
    return False

def verify_data():
    session = requests.Session()
    
    # 1. Login
    log("\n🔐 Logging in...")
    try:
        login_resp = session.post(f"{BASE_URL}/auth/login", json={
            "email": "joao@example.com",
            "senha": "senha123"
        })
        
        if login_resp.status_code != 200:
            log(f"❌ Login failed: {login_resp.text}")
            return False
            
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        log("✅ Login successful!")
        
        # 2. Get Contas
        log("💰 Fetching accounts...")
        contas_resp = session.get(f"{BASE_URL}/contas", headers=headers)
        if contas_resp.status_code == 200:
            contas = contas_resp.json()
            log(f"✅ Found {len(contas)} accounts")
            for c in contas:
                log(f"   - {c['nome']}: R$ {c['saldo']}")
        else:
            log(f"❌ Failed to fetch accounts: {contas_resp.text}")
            return False

        # 3. Get Transacoes
        log("💸 Fetching transactions...")
        trans_resp = session.get(f"{BASE_URL}/transacoes", headers=headers)
        if trans_resp.status_code == 200:
            trans = trans_resp.json()
            log(f"✅ Found {len(trans)} transactions")
        else:
            log(f"❌ Failed to fetch transactions: {trans_resp.text}")
            return False
            
        return True

    except Exception as e:
        log(f"❌ Error verifying data: {e}")
        return False

def seed_db():
    log("\n🌱 Seeding database...")
    try:
        resp = requests.post(f"{BASE_URL}/seed")
        if resp.status_code == 200:
            log("✅ Database seeded successfully!")
        elif resp.status_code == 400 or "Banco já contém dados" in resp.text:
             log("⚠️ Database already has data.")
        else:
            log(f"❌ Seed failed: {resp.text}")
    except Exception as e:
        log(f"❌ Error seeding database: {e}")

if __name__ == "__main__":
    # Clear log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("--- Verification Started ---\n")

    if wait_for_api():
        seed_db()
        if verify_data():
            log("\n🎉 API Verification SUCCESS!")
        else:
            log("\n❌ API Verification FAILED.")
            sys.exit(1)
    else:
        sys.exit(1)
