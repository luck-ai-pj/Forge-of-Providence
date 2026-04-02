import pathlib

def convert_rates(txt: str) -> str:
  lines = [l.strip() for l in txt.splitlines() if l.strip()]

  i = 0
  assert lines[i] == "[Success Rate]"
  i += 1

  headers = lines[i].split()[1:]
  i += 1

  success = {g: {} for g in headers}

  while i < len(lines) and not lines[i].startswith("["):
    parts = lines[i].split()
    enchant = int(parts[0])
    for g, v in zip(headers, parts[1:]):
      success[g][enchant] = float(v)
    i += 1

  assert lines[i] == "[Destroy Rate]"
  i += 1

  destroy = {}
  while i < len(lines):
    g, v = lines[i].split()
    destroy[g] = float(v)
    i += 1

  out = []

  for g in headers:
    out.append(f"[{g}]")
    for enchant in sorted(success[g].keys()):
      s = success[g][enchant]
      d = destroy.get(g, 0.0)
      m = max(0, 100 - s - d)

      out.append(
        f"Enchant {enchant} -> {enchant+1}: "
        f"Success {s:g}%, Maintain {m:g}%, Destroy {d:g}%"
      )
    out.append("")

  return "\n".join(out)


# ===== 실행 =====
root = pathlib.Path(__file__).resolve().parents[1]

src = root / "docs/prob_dev.txt"
dst = root / "docs/prob.txt"

dst.write_text(convert_rates(src.read_text(encoding="utf-8")), encoding="utf-8")
