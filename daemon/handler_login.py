import json
from .session_store import create_session, get_user_from_session

# ==========================================
#  LOGIN HANDLER
# ==========================================
def handle_login(username):
    sid = create_session(username, ttl=3600)
    headers = {
        "Set-Cookie": f"sessionid={sid}; HttpOnly; Path=/; Max-Age=3600",
        "Content-Type": "text/plain; charset=utf-8",
    }
    body = b"Login OK"
    status = "200 OK"
    return status, headers, body

# ==========================================
#  USER INFO HANDLER
# ==========================================
def handle_submit_info(user, body):
    if not user:
        body_html = (
            '<h1>401 Unauthorized</h1>'
            '<p>Login required. <a href="/login">Login</a></p>'
        )
        headers = {"Content-Type": "text/html; charset=utf-8"}
        return "401 Unauthorized", headers, body_html

    try:
        data = json.loads(body)
        print(f"[INFO] User {user} updated info: {data}")
        resp = {"message": "User info updated", "data": data}
        headers = {"Content-Type": "application/json"}
        body = json.dumps(resp)
        return "200 OK", headers, body
    except Exception as e:
        headers = {"Content-Type": "text/plain"}
        return "400 Bad Request", headers, str(e)

# ==========================================
#  LIST MANAGEMENT HANDLERS
# ==========================================
_global_list = []

def handle_add_list(user, body):
    # if not user:
    #     body_html = (
    #         '<h1>401 Unauthorized</h1>'
    #         '<p>Login required. <a href="/login">Login</a></p>'
    #     )
    #     headers = {"Content-Type": "text/html; charset=utf-8"}
    #     return "401 Unauthorized", headers, body_html

    try:
        data = json.loads(body)
        item = data.get("item")
        if not item:
            raise ValueError("Missing 'item'")
        _global_list.append({"user": user, "item": item})
        resp = {"message": "Item added", "item": item}
        headers = {"Content-Type": "application/json"}
        body = json.dumps(resp)
        return "200 OK", headers, body
    except Exception as e:
        headers = {"Content-Type": "text/plain"}
        return "400 Bad Request", headers, str(e)

def handle_get_list(user):
    # if not user:
    #     body_html = (
    #         '<h1>401 Unauthorized</h1>'
    #         '<p>Login required. <a href="/login">Login</a></p>'
    #     )
    #     headers = {"Content-Type": "text/html; charset=utf-8"}
    #     return "401 Unauthorized", headers, body_html

    resp = {"count": len(_global_list), "list": _global_list}
    headers = {"Content-Type": "application/json"}
    body = json.dumps(resp)
    return "200 OK", headers, body

# ==========================================
#  P2P MANAGEMENT HANDLERS
# ==========================================
_peers = {}
_messages = []

def handle_connect_peer(user, body):
    headers = {
       
    }
    body = b"Login OK"
    status = "200 OK"
    return status, headers, body

def handle_get_messages(user):
    if not user:
        body_html = (
            '<h1>401 Unauthorized</h1>'
            '<p>Login required. <a href="/login">Login</a></p>'
        )
        headers = {"Content-Type": "text/html; charset=utf-8"}
        return "401 Unauthorized", headers, body_html

    msgs = [m for m in _messages if m["to"] == user or m["from"] == user]
    resp = {"count": len(msgs), "messages": msgs}
    headers = {"Content-Type": "application/json"}
    body = json.dumps(resp)
    return "200 OK", headers, body
