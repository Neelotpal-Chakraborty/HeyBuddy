import json
try:
    import google.generativeai as genai
    info = {'found': True, 'dir': [n for n in dir(genai) if not n.startswith('_')][:400]}
    try:
        import pkg_resources
        ver = pkg_resources.get_distribution('google-generativeai').version
    except Exception:
        ver = None
    info['version'] = ver
except Exception as e:
    info = {'found': False, 'error': repr(e)}
print(json.dumps(info, indent=2))
