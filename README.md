# PlayList

Memories, Discoveries からプレイリストを作成する

## 使い方

```bash
# Shopify で作成したクライアントIDを .env を記載する
cp .env.sample .env

# ブラウザで Auth URL を開き認証する
docker run --rm -it -p 27228:27228 --env-file ./.env ghcr.io/conradludgate/spotify-auth-proxy

# APIKey を terraform.tfvars に記載する
cd workloads/playlist
cp terraform.tfvars.sample terraform.tfvars

terraform apply
```
