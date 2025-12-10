import importlib, os, json
mods = [
    'deepagents',
    'deepagents.llms',
    'deepagents.llms.gemini',
    'deepagents.agents',
    'deepagents.agents.deepagent',
    'google.generativeai',
]
results = {}
for m in mods:
    try:
        spec = importlib.util.find_spec(m)
        info = {'found': bool(spec), 'origin': spec.origin if spec else None}
        try:
            mod = importlib.import_module(m)
            attrs = [x for x in dir(mod) if not x.startswith('_')]
            info['attrs_sample'] = attrs[:40]
        except Exception as e:
            info['import_error'] = repr(e)
    except Exception as e:
        info = {'found': False, 'error': repr(e)}
    results[m] = info
results['GEMINI_API_KEY'] = bool(os.getenv('GEMINI_API_KEY'))
print(json.dumps(results, indent=2))
