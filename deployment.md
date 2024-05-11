# Path of Modifiers - Deployment

## Setting up environment variables 

To set the env variables, copy the `temp.env` file and name it `.env`. Follow the steps to set the `changethis` variables in [Generate secret keys](#generate-secret-keys)

### <a id="generate-secret-keys"></a> Generate secret keys

Some environment variables in the `.env` file have a default value of `changethis`.

You have to change them with a secret key, to generate secret keys you can run the following command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the content and use that as password / secret key. And run that again to generate another secure key.
