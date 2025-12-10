import google.generativeai as genai, json
keys = ['ChatSession','GenerativeModel','responder','get_model','get_base_model','types']
out={}
for k in keys:
    try:
        obj = getattr(genai, k)
        out[k] = {'repr': repr(obj), 'dir': [n for n in dir(obj) if not n.startswith('_')][:400]}
    except Exception as e:
        out[k] = {'error': repr(e)}
print(json.dumps(out, indent=2))
