import argparse, json
from jsonschema import Draft202012Validator

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--file', required=True, help='Path to JSONL file to validate')
    ap.add_argument('--schema', default='src/schema/unified_post_schema.json')
    args = ap.parse_args()

    with open(args.schema, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)

    errors = 0
    with open(args.file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            obj = json.loads(line)
            for err in validator.iter_errors(obj):
                print(f'Line {i} validation error: {err.message} at {".".join(map(str, err.path))}')
                errors += 1
    if errors == 0:
        print('OK: file conforms to schema')
    else:
        print(f'Found {errors} validation issues')

if __name__ == '__main__':
    main()
