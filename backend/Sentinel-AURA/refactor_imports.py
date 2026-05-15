import re
from pathlib import Path

root = Path('aura_risk_engine')
package_names = {
    'app',
    'alert_response_engine',
    'crowd_intelligence',
    'incident_intelligence',
    'light_intelligence',
    'realtime_orchestrator',
    'risk_engine',
    'route_safety_engine',
    'testing_framework',
}

# Process package files and root-level tests
paths = list(root.rglob('*.py')) + list(Path('.').glob('*.py'))
for path in paths:
    if path.name == 'refactor_imports.py':
        continue
    text = path.read_text(encoding='utf-8')
    package_parts = None
    if path.parts[0] == 'aura_risk_engine':
        package_parts = path.relative_to(root).parent.parts
    new_lines = []
    changed = False
    for line in text.splitlines(True):
        orig = line
        # absolute package imports
        if re.match(r'\s*from\s+app\.', line):
            line = re.sub(r'^(\s*)from\s+app\.', r'\1from aura_risk_engine.app.', line)
        m = re.match(r'^(\s*)from\s+(' + '|'.join(package_names) + r')\b', line)
        if m:
            indent, module = m.groups()
            line = re.sub(r'^(\s*)from\s+' + module, rf'\1from aura_risk_engine.{module}', line)
        if package_parts is not None:
            m = re.match(r'^(\s*)from\s+(\.+)([A-Za-z_][A-Za-z0-9_]*)', line)
            if m:
                indent, dots, module = m.groups()
                level = len(dots)
                if level <= len(package_parts) + 1:
                    base = package_parts[: len(package_parts) - (level - 1)]
                    target = '.'.join(['aura_risk_engine'] + list(base) + [module])
                    line = f'{indent}from {target}' + line[m.end(0):]
        if line != orig:
            changed = True
        new_lines.append(line)
    if changed:
        path.write_text(''.join(new_lines), encoding='utf-8')
