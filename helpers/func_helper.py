from functools import partial

def _t(f, m: str):
  print(f'{m}: {f}')
  return f

trace = lambda msg: partial(_t, m=msg)
