# simiotics-s3

This repository contains the code for the `simiotics_s3` tool, which you can use to sanely share
datasets with your friends - both human and machine (especially machine)!

It does so using [AWS S3](https://aws.amazon.com/s3/) in combination with a Simiotics data registry.

## Installation

We recommend you use virtual environments. If you are using a recent Python3, you can create a
virtual environment wherever you would like:
```
python3 -m venv <desired-venv-directory>
```

Then, to activate:
```
. <desired-venv-directory>/bin/activate
```

### Installation from PyPI

`simiotics_s3` can be installed from PyPI:
```
pip3 install simiotics-s3
```

### Installation from source code

From the root of this repository:
```
pip3 install -e .
```


## Usage

### Simiotics data registry

To use this tool, you will need to specify a Simiotics data registry in which you will register your
data and your datasets. Our customers use private registries hosted on their own infrastructure. If
you don't have access to such a private registry and would like to experiment with our tool, you can
use our public alpha registry. Just set the
`SIMIOTICS_DATA_REGISTRY` environment variable:
```
export SIMIOTICS_DATA_REGISTRY=registry-alpha.simiotics.com:7010
```

### S3

The `simiotics_s3` tool is BYOB (bring your own bucket). The data will be hosted on your own S3
bucket. The tool will use a Simiotics data registry to index your S3 blobs and share them with
others in the form of datasets.

`simiotics_s3` uses the [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
library under the hood and you will have to provide it with credentials that it can use to
authenticate against the bucket. One way to do this is to export the `AWS_ACCESS_KEY_ID` and
`AWS_SECRET_ACCESS_KEY` environment variables, which can be populated with values from your AWS
credentials file (on Linux or Mac, try `less ~/.aws/credentials`).

Run:
```
export AWS_ACCESS_KEY_ID=<COPYPASTA YOUR ACCCESS KEY ID HERE>
export AWS_SECRET_ACCESS_KEY=<COPYPASTA YOUR SECRET ACCCESS KEY HERE>
```

### Workflow

In the commands below, replace:
1. `<UNIQUE SOURCE ID>` with a name that you would like to give your source
2. `<SOURCE S3 ROOT>` with an S3 path of the form `s3://<BUCKET>/<KEY_PREFIX>` (e.g.
`s3://simiotics-is-awesome/source/goes/here`)
3. `<DOWNLOAD DIR>` with the path to the directory into which you'd like to download data

Register a source (which you can also think of as a dataset). It will be empty at first. This is
okay. After all, sources change over time.

```
simiotics_s3 sources create --id <UNIQUE SOURCE ID> --s3-path <SOURCE S3 ROOT>
```

If your ID was truly unique, you should see a response like this:
```
*** Source registered ***
id: "first-source"
source_type: SOURCE_S3
data_access_spec: "s3://simiotics-test/first-source"
created_at {
  seconds: 1568050335
  nanos: 766883136
}
```

Register a bunch of data files against the source like this:
```
simiotics_s3 data register --source <UNIQUE SOURCE ID> <FILE PATHS>
```

To download all the data registered under a given source, you can use the `simiotics_s3 data download`
command. Anyone that has access to both the S3 bucket hosting the data and the Simiotics data registry
can do this. Humans, servers, docker containers -- Simiotics has no prejudices and neither does S3!

```
simiotics_s3 data download --source <UNIQUE SOURCE ID> --dir <DOWNLOAD DIR>
```

Check that the data has been downloaded:
```
ls <DOWNLOAD DIR>
```

Model away. :)
