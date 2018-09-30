## CodeStar Memo

### enable share deployment of cloud9 and CodePipeline

Check the role used in cloudFormation stack.(CloudFormation->stack->abstract->IAM Role)
If the role is created by pipeline, permit the role to access cloud9 bucket (default.cloud9-{accountid}-sam-deployments-{region})
else if the role is created by cloud9, permit the role to access pipeline bucke (default. aws-codestar-{region}-{accountid}-{pj-name}-pipe)

### enable cross region access to S3 bucket for CodeBuild process

The deploy package must put to bucket in region of lambda deployment target region.
The bucket must have following bucket policy which allow CodeBuild role to access the bucket.
CodeBuild role must have permission policy to access s3 buckets.

S3 bucket policy
~~~
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Cross Region permissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{account}:role/CodeStarWorker-mycodestar-CodeBuild"
            },
            "Action": "*",
            "Resource": [
                "arn:aws:s3:::{bucket}",
                "arn:aws:s3:::{bucket}/*"
            ]
        }
    ]
}
~~~
[aws doc](https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/dev/example-walkthroughs-managing-access-example2.html)



### pytest

~~~
Suzuki:~/environment/myCodeStar (master) $ pytest tests -v
================================================= test session starts =================================================
platform linux -- Python 3.6.5, pytest-3.8.0, py-1.6.0, pluggy-0.7.1 -- /usr/bin/python3.6
cachedir: .pytest_cache
rootdir: /home/ec2-user/environment/myCodeStar, inifile: pytest.ini
collected 3 items                                                                                                     

tests/test_handler.py::test_index_handler_heroes PASSED                                                         [ 33%]
tests/test_handler.py::test_index_handler_annotations PASSED                                                    [ 66%]
tests/test_handler.py::test_index_handler_objdetect PASSED                                                      [100%]

============================================== 3 passed in 1.28 seconds ===============================================
Suzuki:~/environment/myCodeStar (master) $ 
~~~

## Coverage

~~~
Suzuki:~/environment/myCodeStar (master) $ coverage report --omit='/usr/*,*/site-packages/*,*/dist-packages*,tests/*' -m
Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/annotations.py                              54     27    50%   23-25, 36-66
src/common.py                                   53     20    62%   29-30, 33-36, 45-52, 56-63, 66-71
src/heroes.py                                   56     34    39%   25-26, 36-76
src/index.py                                    28      7    75%   26-34
src/object_detection/__init__.py                 0      0   100%
src/object_detection/tf_objectdetection.py     107     87    19%   10-18, 21-29, 42-43, 47-71, 75-83, 85-89, 91-117, 122-126, 131-153
src/upload.py                                   22     14    36%   13-29
--------------------------------------------------------------------------
TOTAL                                          320    189    41%
Suzuki:~/environment/myCodeStar (master) $ 
~~~