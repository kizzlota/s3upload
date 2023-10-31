# s3upload

### Home work Vladimir Pyrig

#### build:

```shell
poetry build
```
#### install with poetry:

```shell
poetry add dist/s3upload-0.1.0-py3-none-any.whl
```
#### OR install with pip:  
```shell
pip install dist/s3upload-0.1.0-py3-none-any.whl
```
#### Call the utility:
```shell
s3upload --help 
```


### Utility accepts params:

* `--url` or `-u` URL to download file and can be repeated, required.
* `--bucket` or `-b` AWS bucket name, required.
* `--workers` or `-w` Number of workers default 2
* `--aws-key` or `-r` AWS key
* `--aws-secret` or `-s` AWS secret
* `--aws-region` or `-r` AWS region
 
## Thanks for your attention 