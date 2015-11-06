# reliable_executor

## Running tests

```bash
python setup.py test
```

## Building binary distribution

```bash
python setup.py bdist_wheel
```

## Running

```python
import reliable_executor

reliable_executor.reliably_execute(fn, args)
```
