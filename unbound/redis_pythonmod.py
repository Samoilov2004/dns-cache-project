import json
import os
import redis

redis_client = None

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# TTL, который будет отдаваться клиенту в DNS-ответе,
# когда ответ берется из Redis
RETURN_TTL = int(os.getenv("RETURN_TTL", "60"))


def init_standard(id, env):
    global redis_client
    try:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
        redis_client.ping()
        log_info(f"redis_pythonmod: connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
        return True
    except Exception as e:
        log_err(f"redis_pythonmod init failed: {e}")
        return False


def deinit(id):
    log_info("redis_pythonmod: deinit")
    return True


def inform_super(id, qstate, superqstate, qdata):
    return True


def _normalize_qname(name: str) -> str:
    name = name.strip().lower()
    if not name.endswith("."):
        name += "."
    return name


def _key(qname: str, qtype: str) -> str:
    return f"dns:cache:{qname}:{qtype}"


def _build_a_response(qstate, qname: str, answers: list) -> bool:
    msg = DNSMessage(qname, RR_TYPE_A, RR_CLASS_IN, PKT_QR | PKT_RA)

    for ans in answers:
        name = ans.get("name", qname)
        data = ans["data"]
        msg.answer.append(f"{name} {RETURN_TTL} IN A {data}")

    if not msg.set_return_msg(qstate):
        log_err("redis_pythonmod: set_return_msg failed")
        return False

    qstate.return_rcode = RCODE_NOERROR

    # Как в официальном hello world примере
    if qstate.return_msg:
        qstate.return_msg.rep.security = 2

    return True


def operate(id, event, qstate, qdata):
    global redis_client

    if event == MODULE_EVENT_NEW or event == MODULE_EVENT_PASS:
        try:
            qname = _normalize_qname(qstate.qinfo.qname_str)
            qtype_num = qstate.qinfo.qtype

            # Пока поддерживаем только A-записи
            if qtype_num != RR_TYPE_A:
                qstate.ext_state[id] = MODULE_WAIT_MODULE
                return True

            key = _key(qname, "A")
            raw = redis_client.get(key)

            if raw is not None:
                entry = json.loads(raw)
                answers = entry.get("answers", [])

                if answers:
                    if _build_a_response(qstate, qname, answers):
                        log_info(f"redis_hit qname={qname} qtype=A key={key}")
                        qstate.ext_state[id] = MODULE_FINISHED
                        return True

            log_info(f"redis_miss qname={qname} qtype=A key={key}")
            qstate.ext_state[id] = MODULE_WAIT_MODULE
            return True

        except Exception as e:
            log_err(f"redis_pythonmod operate error: {e}")
            qstate.ext_state[id] = MODULE_WAIT_MODULE
            return True

    elif event == MODULE_EVENT_MODDONE:
        qstate.ext_state[id] = MODULE_FINISHED
        return True

    else:
        qstate.ext_state[id] = MODULE_WAIT_MODULE
        return True
