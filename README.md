# AMI-Amigos-Cloud-Project

A Python ETL pipeline that fetches Pokemon data from the PokeAPI, stores it in MongoDB hosted on an EC2 instance, and uploads it to AWS S3.

## Pipeline

```
PokeAPI --> Python --> MongoDB (EC2) --> JSON Export --> AWS S3
```

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- AWS credentials configured (see below)
- SSH key for EC2 instance (see below)

## AWS Setup

### Credentials

Configure your AWS credentials using the CLI:

```bash
aws configure
```

This will prompt for your access key, secret key, region, and output format. Alternatively, set them manually:

`~/.aws/credentials`:
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

`~/.aws/config`:
```ini
[default]
region = eu-west-1
output = json
```

To verify your credentials are working:

```python
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

s3_client = boto3.client('s3')

try:
    bucket_list = s3_client.list_buckets()
    print("Credentials valid. Buckets:", [b['Name'] for b in bucket_list['Buckets']])
except NoCredentialsError:
    print("No credentials found — check your ~/.aws/credentials file.")
except ClientError as e:
    print("Credentials rejected by AWS:", e.response['Error']['Message'])
```

### SSH Key

Place your EC2 key pair `.pem` file at `~/.ssh/your-key-pair.pem` and update the path in `.env`:

```
EC2_IP=your-ec2-public-ip
```

The key path in `main.py` defaults to `~/.ssh/se-louis-key-pair.pem` — update this to match your own key file name.

## Install dependencies

```bash
uv sync
```

## Run the pipeline

```bash
uv run main.py
```

This will:
1. Fetch all Pokemon from the PokeAPI
2. Store them in MongoDB on the EC2 instance
3. Export the data as JSON
4. Upload it to the S3 bucket under `AMI-Amigos/pokemon.json`

## Run CRUD tests (local MongoDB)

Requires MongoDB running locally on port 27017. Run in order:

```bash
uv run test_create.py
uv run test_read.py
uv run test_update.py
uv run test_delete.py
```

## S3 Bucket

Data is uploaded to: `se-data-with-ai-etl-project/AMI-Amigos/`

## Data Notes

Each Pokemon document stored in MongoDB contains only `name` and `url` fields from the PokeAPI. Full details (id, height, weight, base experience, moves, sprites etc.) were intentionally omitted as the full payload per Pokemon is extremely large and would make the dataset impractical to store and export.

The `get_pokemon_details()` function exists in the code but is not called in the main pipeline for this reason.

JSON serialization uses `bson.json_util.dumps` instead of the standard `json.dumps` to correctly handle MongoDB's BSON types (e.g. ObjectId).
