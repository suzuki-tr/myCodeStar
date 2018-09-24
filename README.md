## CodeStar Memo

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






